from com.platform.utilities.logger import Logger
from com.platform.utilities.bigquery import Bigquery
from com.platform.constants.placeholders import Placeholder
from com.platform.constants.sql_statements import SqlStatements
from com.platform.constants.common_variables import CommonVariables


def main_log_insert(process_id: int, bigquery: Bigquery, logger: Logger) -> None:

    """Function which inserts an entry in the Reference log table"""

    logger.info("counter.main_log_insert() function getting executed...")

    # Preparing reference sql select statement
    reference_log_query: str = SqlStatements.REF_LOG_INSERT_STATEMENT \
                                .replace(Placeholder.PROCESS_ID.value, process_id) \
                                .replace(Placeholder.BATCH_DATE.value, CommonVariables.DATE)

    # Executes the sql statement
    bigquery.execute_query(reference_log_query)


def main_log_update(process_id: int, status: str, error_message: str, bigquery: Bigquery, logger: Logger):

    """Function which updates last entry in the Reference log table"""

    logger.info("counter.main_log_update() function getting executed...")

    # Preparing reference sql select statement
    reference_log_query: str = SqlStatements.REF_LOG_UPDATE_STATEMENT \
                                .replace(Placeholder.PROCESS_ID.value, process_id) \
                                .replace(Placeholder.BATCH_DATE.value, CommonVariables.DATE) \
                                .replace(Placeholder.LOG_STATUS.value, status) \
                                .replace(Placeholder.LOG_ERROR_MSG.value, error_message)

    # Executes the sql statement
    bigquery.execute_query(reference_log_query)