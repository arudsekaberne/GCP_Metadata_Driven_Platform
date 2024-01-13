import sys
from com.platform.utilities.helper import Helper
from com.platform.utilities.logger import Logger
from com.platform.utilities.storage import Storage
from google.api_core.exceptions import GoogleAPIError
from com.platform.models.reference_model import ReferenceModel
from com.platform.constants.common_variables import CommonVariables


def check_process_mandatory_folders(project_folder: str, storage: Storage, logger: Logger) -> None:

    """Function which check all mandatory folders are in project folder"""

    logger.subtitle("Inspect Bucket")

    # Check mandatry blob exists
    for mandatory_blob in CommonVariables.GCP_MANDATORY_BLOBS:

        mandatory_blob_path = f"{project_folder}/{mandatory_blob}/"

        if not storage.blob_exist(CommonVariables.GCP_BUCKET_NAME, mandatory_blob_path):
            raise GoogleAPIError(f"The mandatory folder '{mandatory_blob_path}' not exists in {CommonVariables.GCP_BUCKET_NAME}.")
        
    logger.info(f"inspector.check_process_mandatory_folders() executed successfully, which guarantees to store log file under user project log folder")
    
    
def is_process_active(is_active: bool, process_name: str, logger: Logger) -> None:
    
    """Check the process active, if not handles the run accordingly"""
    
    if not is_active:
        logger.warning(f"The process '{process_name}' is INACTIVE, please set 'is_active' column to 'true' in {CommonVariables.REF_TABLE_NAME} table to execute checkpoints.")
        # TODO: Send an activation mail
        sys.exit(3)