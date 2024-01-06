from google.cloud.storage import Bucket
from com.platform.utilities.logger import Logger
from com.platform.utilities.storage import Storage
from google.api_core.exceptions import GoogleAPIError
from com.platform.constants.common_variables import CommonVariables


def inspect_bucket(project_folder: str, storage: Storage, logger: Logger) -> None:

    """Function which check all mandatory folders are in project folder"""

    logger.subtitle("Inspect Bucket")

    fmt_project_folder = project_folder.strip("/")
    logger.info(f"Formatted project folder: {fmt_project_folder}")

    # Check mandatry blob exists
    for mandatory_blob in CommonVariables.MANDATORY_BLOBS:

        mandatory_blob_path = f"{fmt_project_folder}/{mandatory_blob}"

        if not storage.blob_exists(CommonVariables.BUCKET_NAME, mandatory_blob_path):
            raise GoogleAPIError(f"The mandatory folder '{mandatory_blob_path}' not exists under {CommonVariables.BUCKET_NAME}.")
    
    