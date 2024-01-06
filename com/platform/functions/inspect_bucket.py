from com.platform.utilities.logger import Logger
from com.platform.utilities.storage import Storage


def inspect_bucket(project_folder: str, storge: Storage, logger: Logger):

    """Function which check all mandatory folders are in project folder"""

    logger.subtitle("Inspect Bucket")

    