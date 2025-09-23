import falcon

from dataclasses import dataclass
from trustyscheduler.log import logger, add_child_logger
from trustyscheduler.utils import Updateable

LOGGER_TASKMAN = "trustytaskmanager"


@dataclass(kw_only=True)
class TrustyTaskManager(Updateable):

    def __init__(self) -> None:
        self.log = add_child_logger(logger, LOGGER_TASKMAN)

    def on_get(self, req: falcon.Request, resp: falcon.Response):
        # on get, return task status based on the id provided
        # on no id, return whole list of tasks with history
        self.log.debug("Processing get request")

        resp.status = falcon.HTTP_200  # This is the default status
        resp.content_type = falcon.MEDIA_JSON  # Default is JSON, so override
        # on get, task manager status
        resp.media = {}

    def on_post(self, req: falcon.Request, resp: falcon.Response):
        # on post, create a new task based on the provided data
        # if task exists, return either error or update based on configuration
        self.log.debug("Processing post request")
        resp.status = falcon.HTTP_201
        resp.content_type = falcon.MEDIA_JSON
        resp.media = {}

    def on_delete(self, req: falcon.Request, resp: falcon.Response):
        # on delete, delete a task based on the id provided
        # task must not be running
        # to cancel a running task, use scheduler endpoint
        self.log.debug("Processing delete request")
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_JSON
        resp.media = {}

    def terminate(self):
        # Clean up resources, stop threads, etc.
        pass

    def get_task_types(self) -> list[str]:
        return []

    def get_total_scheduled_tasks(self) -> int:
        return 0

    def get_total_running_tasks(self) -> int:
        return 0

    def get_total_completed_tasks(self) -> int:
        return 0

    def get_total_failed_tasks(self) -> int:
        return 0
