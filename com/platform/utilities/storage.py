from google.cloud.storage import Bucket, Client
from com.platform.utilities.helper import Helper
from com.platform.utilities.logger import Logger
from com.platform.constants.common_variables import CommonVariables


class Storage():

    """Class which handles all cloud storage executions"""

    def __init__(self, logger: Logger):
        self.logger: Logger = logger
        self.client: Client = Client()
        self.logger.info("Cloud storage client got created")

    
    def __create_bucket_obj(self, bucket_name: str) -> Bucket:

        """Create and return bucket object"""

        return self.client.get_bucket(bucket_name)
    

    def blob_exists(self, bucket_name: str, blob_path: str):

        """Function checks the given complete blob exists inside the given bucket"""

        self.logger.info(f"BLOB EXISTS function getting executed...")
        blob_path: str = f"{blob_path.strip('/')}/"
        self.logger.info(f"Find blob '{blob_path}' in '{bucket_name}'")

        # Create bucket object
        bucket: Bucket = self.__create_bucket_obj(bucket_name)

        # Loop through all blob name
        blob_exist: bool = any([blob.name.startswith(blob_path) for blob in bucket.list_blobs()])
        self.logger.info(f"Blob exist: {blob_exist}")

        return blob_exist
