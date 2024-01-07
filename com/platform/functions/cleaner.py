from typing import List
from google.cloud.storage.blob import Blob
from com.platform.utilities.logger import Logger
from com.platform.utilities.storage import Storage


def clean_log_folder(project_folder: str, retention_count: int, storage: Storage, logger: Logger) -> None:

    """Function cleans user project log folder"""

    __is_log_file = lambda blob: blob.name.endswith(".log")
    
    logger.info("cleaner.clean_log_folder() function getting executed...")

    log_files: List[Blob]        = storage.list_blobs(f"{project_folder}/log")
    sorted_log_files: List[Blob] = sorted(log_files, key = lambda blob: blob.time_created, reverse=True)
    retain_log_files: List[str]  = [sorted_log_file.name
                                        for sorted_log_file in sorted_log_files
                                            if __is_log_file(sorted_log_file)][:retention_count]

    logger.info(f"Log files to be retained: {retain_log_files}")
    
    for _log_file in log_files:

        if (_log_file.name not in retain_log_files) and __is_log_file(_log_file):
            logger.info(f"Expired log {_log_file.name} is getting removed")

            # Delete blob from cloud storage
            _log_file.delete()