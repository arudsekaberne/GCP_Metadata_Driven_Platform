from typing import List
from google.cloud.storage.blob import Blob
from com.platform.utilities.logger import Logger
from com.platform.utilities.storage import Storage


def clean_log_folder(process_id: str, project_folder: str, retention_count: int, storage: Storage, logger: Logger) -> None:

    """Function cleans user project log folder"""
    
    __is_my_log = lambda blob: blob.name.split("/")[-1].startswith(process_id) and blob.name.endswith(".log")
    
    logger.info("cleaner.clean_log_folder() function getting executed...")
    logger.info(f"Number of latest files that starts with '{process_id}' to be retained: {retention_count}")

    log_files: List[Blob]         = storage.list_blobs(f"{project_folder}/log/")
    process_log_files: List[Blob] = [log_file for log_file in log_files if __is_my_log(log_file)]
    sorted_log_files: List[Blob]  = sorted(process_log_files, key = lambda blob: blob.time_created, reverse=True)
    retain_log_files: list[str]   = [log_file.name for log_file in sorted_log_files[:retention_count]]
    
    for log_file in sorted_log_files:
        if log_file.name not in retain_log_files:
            logger.info(f"Expired log {log_file.name} is getting removed")

            # Delete blob from cloud storage
            log_file.delete()