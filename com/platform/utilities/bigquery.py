from com.platform.utilities.helper import Helper
from com.platform.utilities.logger import Logger
from com.platform.utilities.storage import Storage
from google.cloud.bigquery.table import RowIterator
from google.cloud.bigquery import Client, QueryJob, Row
from com.platform.constants.common_variables import CommonVariables


class Bigquery():

    """Class which handles all bigquery executions"""

    def __init__(self, logger: Logger):
        self.logger: Logger = logger
        self.client: Client = Client()
        self.logger.info("Bigquery client got created")


    def select_query(self, query: str) -> list:

        """Function which takes select query as input and returns the result as output"""

        self.logger.info("Bigquery.select_query() function getting executed...")
        self.logger.info(f"Query: {query}")

        # Makes an API request
        query_job: QueryJob = self.client.query(query)
        
        # Wait for query job to complete
        query_result: RowIterator    = query_job.result()
        query_result_list: list[Row] = list(query_result)
        
        self.logger.info(f"Query returned {len(query_result_list)} record{Helper.singular_or_plural(len(query_result_list))}")

        self.logger.info("Bigquery.select_query() executed successfully")

        return query_result_list
    

    def execute_query(self, query: str) -> None:

        """Function which takes any biqguery statement as input and executes them"""

        self.logger.info("Bigquery.execute_query() function getting executed...")
        self.logger.info(f"Query: {query}")

        # Makes an API request
        query_job: QueryJob = self.client.query(query)
        
        # Wait for query job to complete
        query_job.result()

        self.logger.info("Bigquery.execute_query() function executed successfully")


    def execute_file(self, project_folder: str, sql_file: str, storage: Storage) -> None:

        """Function which takes a sql file as input and executes them"""

        self.logger.info("Bigquery.execute_file() function getting executed...")

        file_query: str = storage.bucket.blob(f"{project_folder}/{CommonVariables.GCP_SCRIPT_DIR_NAME}/{sql_file}").download_as_text()

        self.execute_query(file_query)

        self.logger.info("Bigquery.execute_file() function executed successfully")

