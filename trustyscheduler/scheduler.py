import falcon

from dataclasses import dataclass

from trustyscheduler.log import logger, add_child_logger
from trustyscheduler.utils import Updateable

LOGGER_SCHEDULER = "trustyscheduler"


@dataclass(kw_only=True)
class TrustyScheduler(Updateable):
    def __init__(self) -> None:
        self.log = add_child_logger(logger, LOGGER_SCHEDULER)

    def on_get(self, req: falcon.Request, resp: falcon.Response):
        # on get, return scheduler status with upcoming scheduled tasks
        self.log.debug("Processing get request")
        resp.status = falcon.HTTP_200  # This is the default status
        resp.content_type = falcon.MEDIA_JSON  # Default is JSON, so override
        # on get, return scheduler status
        resp.media = {}

    def on_post(self, req: falcon.Request, resp: falcon.Response):
        # on post, schedule a new task based on the provided data
        # if task exists, return either error or update based on configuration
        self.log.debug("Processing post request")
        resp.status = falcon.HTTP_201
        resp.content_type = falcon.MEDIA_JSON
        resp.media = {}

    def on_delete(self, req: falcon.Request, resp: falcon.Response):
        # on delete, cancel a running task based on the id provided
        # but not delete it from history
        self.log.debug("Processing delete request")
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_JSON
        resp.media = {}

    def terminate(self):
        # Clean up resources, stop threads, etc.
        pass
