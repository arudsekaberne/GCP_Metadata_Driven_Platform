from com.platform.utilities.helper import Helper
from com.platform.utilities.logger import Logger
from google.cloud.bigquery.table import RowIterator
from google.cloud.bigquery import Client, QueryJob, Row


class Bigquery():

    """Class which handles all bigquery executions"""

    def __init__(self, logger: Logger):
        self.logger: Logger = logger
        self.client: Client = Client()
        self.logger.info("Bigquery client got created")


    def select_query(self, query: str) -> list:

        """Function which takes select query as input and returns the result as output"""

        self.logger.info("SELECT QUERY function getting executed...")
        self.logger.info(f"QUERY: {query}")

        # Makes an API request
        query_job: QueryJob = self.client.query(query)
        
        # Wait for query job to complete
        query_result: RowIterator    = query_job.result()
        query_result_list: list[Row] = list(query_result)
        
        self.logger.info(f"QUERY: Returned {len(query_result_list)} record{Helper.singular_or_plural(len(query_result_list))}")

        return query_result_list
    

    def execute_query(self, query: str) -> None:

        """Function which takes any biqguery statement as input and executes them"""

        # Makes an API request
        query_job: QueryJob = self.client.query(query)
        
        # Wait for query job to complete
        query_job.result()


    def execute_file(self, sql_file: str) -> None:

        """Function which takes a sql file as input and executes them"""

        pass