from typing import List
from com.platform.utilities.helper import Helper
from com.platform.utilities.logger import Logger
from google.cloud.storage import Bucket, Client, blob
from com.platform.constants.common_variables import CommonVariables


class Storage():

    """Class which handles all cloud storage executions"""

    def __init__(self, logger: Logger):
        self.logger: Logger = logger
        self.client: Client = Client()
        self.bucket: Bucket = self.client.get_bucket(CommonVariables.GCP_BUCKET_NAME)
        self.logger.info("Cloud storage client got created")
    

    def list_blobs(self, folder=None) -> List[blob.Blob]:
        """Function return all blob name under given folder"""
        self.logger.info(f"Storage.list_blobs() function getting executed to list blobs under '{folder if folder else CommonVariables.GCP_BUCKET_NAME}'")
        return list(self.bucket.list_blobs(prefix=folder))

    def blob_exist(self, bucket_name: str, bucket_folder: str):

        """Function checks the blob inside the bucket"""

        self.logger.info(f"Storage.blob_exists() function getting executed...")
        self.logger.info(f"Find blob '{bucket_folder}' in {bucket_name}")

        # Loop through all blob name
        for blob in self.list_blobs():
            if blob.name.startswith(bucket_folder):
                self.logger.info(f"Blob exist: {blob}")
                return True
            
        self.logger.info(f"Blob not exist: {bucket_folder}")
        return False
    

    def upload_file(self, source_file_path: str, target_bucket_folder: str) -> None:

        """Function which uploads any file into google cloud storage"""

        self.logger.info(f"Storage.upload_file() function getting executed...")

        target_file_name: str = Helper.extract_file_name(source_file_path)

        # Creates blob file from source file
        blob = self.bucket.blob(f"{Helper.strip_path(target_bucket_folder)}/{target_file_name}")
        
        # Upload the file
        blob.upload_from_filename(source_file_path)
        self.logger.info(f"File '{target_file_name}' got uploaded into '{target_bucket_folder}'")

