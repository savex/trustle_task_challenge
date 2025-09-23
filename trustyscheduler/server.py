import signal
import json
import falcon

from dataclasses import dataclass
from datetime import datetime
from functools import partial
from falcon import media
from wsgiref.simple_server import make_server

from trustyscheduler.log import logger, add_child_logger
from trustyscheduler.taskman import TrustyTaskManager
from trustyscheduler.scheduler import TrustyScheduler
from trustyscheduler.utils import NpEncoder, Updateable


LOGGER_STARTUP = "trustyserver.startup"
LOGGER_SERVER = "trustyserver"


@dataclass(kw_only=True)
class TrustyServer(Updateable):
    app_name: str = "TrustyServer"
    web_port: int = 8080
    started_at: float = 0.0

    def initialize(self) -> None:
        self.log = add_child_logger(logger, LOGGER_SERVER)
        self.tskman = None  # type: TrustyTaskManager | None
        self.schdlr = None  # type: TrustyScheduler | None
        self.started_at = datetime.now().timestamp()

    def on_get(self, req: falcon.Request, resp: falcon.Response):
        self.log.debug("Processing get request")
        resp.status = falcon.HTTP_200  # This is the default status
        resp.content_type = falcon.MEDIA_JSON  # Default is JSON, so override
        # on get, return status of the server
        resp.media = self.status()

    def status(self) -> dict:
        """Returns the status of the server
        Exanmple response:
        {
            "app_name": "TrustyServer",
            "web_port": 8080,
            "started_at": "2023-10-05T12:34:56.789012",
            "uptime_seconds": 12345.67,
            "task_types": [],
            "total_scheduled_tasks": 0,
            "total_running_tasks": 0,
            "total_completed_tasks": 0,
            "total_failed_tasks": 0
        }
        """
        # using a lot of inline calls for illustration;
        # can be broken out as needed
        return {
            "app_name": self.app_name,
            "web_port": self.web_port,
            "started_at": datetime.fromtimestamp(self.started_at).isoformat(),
            "uptime_seconds": datetime.now().timestamp() - self.started_at,
            "task_types": self.tskman.get_task_types() if self.tskman else [],
            "total_scheduled_tasks":
                self.tskman.get_total_scheduled_tasks()if self.tskman else 0,
            "total_running_tasks":
                self.tskman.get_total_running_tasks() if self.tskman else 0,
            "total_completed_tasks":
                self.tskman.get_total_completed_tasks()
                if self.tskman else 0,
            "total_failed_tasks":
                self.tskman.get_total_failed_tasks() if self.tskman else 0
        }


def start_webserver():
    log = add_child_logger(logger, LOGGER_STARTUP)
    if not log:
        raise RuntimeError("Failed to create startup logger")

    def terminate_handler(signum, frame):
        """SIGTERM handler"""
        signame = signal.Signals(signum).name
        log.info(f"{signame} ({signum}) received, terminating threads")
        if server_app.tskman:
            server_app.tskman.terminate()
        if server_app.schdlr:
            server_app.schdlr.terminate()

    def add_route(route: str,
                  handler: TrustyServer | TrustyTaskManager | TrustyScheduler
                  ) -> None:
        logger.debug(f"Registering handler for '{route}' as {type(handler)}")
        app.add_route(route, handler)

    app = falcon.App()
    json_handler = media.JSONHandler(
        dumps=partial(
            json.dumps,
            cls=NpEncoder,
            sort_keys=True,
        ),
    )
    extra_handlers = {
        "application/json": json_handler,
    }

    app = falcon.App()
    app.req_options.media_handlers.update(extra_handlers)
    app.resp_options.media_handlers.update(extra_handlers)

    server_app = TrustyServer()
    server_app.initialize()

    # Add subpages
    log.debug("Initializing Task Manager")
    server_app.tskman = TrustyTaskManager()
    log.debug("Initializing Scheduler")
    server_app.schdlr = TrustyScheduler()
    add_route("/", server_app)
    add_route("/task", server_app.tskman)
    add_route("/scheduler", server_app.schdlr)

    # Create and run service
    with make_server("", server_app.web_port, app) as httpd:
        # Serve until process is killed, SGTERM received or Keyboard interrupt
        try:
            log.debug("Registering SIGTERM")
            signal.signal(signal.SIGTERM, terminate_handler)
            log.info(f"Serving on port {server_app.web_port}...")
            httpd.serve_forever()
        except KeyboardInterrupt:
            log.info("Got keyboard interupt, exiting")
            server_app.tskman.terminate()
            server_app.schdlr.terminate()
