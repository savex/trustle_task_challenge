# Trustle task
# Author: Alex Savatieiev (a.savex@gmail.com)
# Sep 2025

from trustyscheduler.const import title
from trustyscheduler.log import logger_cli
from trustyscheduler.server import start_webserver


def run() -> None:
    logger_cli.info(f"Running {title}")

    # Run code
    start_webserver()

    logger_cli.info("Done")
    return
