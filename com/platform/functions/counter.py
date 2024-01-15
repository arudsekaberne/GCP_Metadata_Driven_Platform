import json
from com.platform.utilities.logger import Logger
from com.platform.utilities.bigquery import Bigquery
from com.platform.constants.placeholders import Placeholder
from com.platform.constants.sql_statements import SqlStatements
from com.platform.constants.common_variables import CommonVariables


def reference_log_insert(process_id: int, batch_date: str, bigquery: Bigquery, logger: Logger) -> None:

    """Function which inserts an entry in the Reference log table"""

    logger.subtitle("Reference Log Insert")
    logger.info("counter.reference_log_insert() function getting executed...")

    # Preparing reference sql select statement
    reference_log_query: str = SqlStatements.REF_LOG_INSERT_STATEMENT \
                                .replace(Placeholder.PROCESS_ID.value, process_id) \
                                .replace(Placeholder.BATCH_DATE.value, batch_date)

    # Executes the sql statement
    bigquery.execute_query(reference_log_query)

    logger.info("counter.reference_log_insert() function executed successfully")


def reference_log_update(process_id: int,  batch_date: str, status: str, error_message: str, bigquery: Bigquery, logger: Logger) -> None:

    """Function which updates last entry in the Reference log table"""

    logger.subtitle("Reference Log Update")
    logger.info("counter.reference_log_update() function getting executed...")

    # Preparing reference sql select statement
    reference_log_query: str = SqlStatements.REF_LOG_UPDATE_STATEMENT \
                                .replace(Placeholder.PROCESS_ID.value, process_id) \
                                .replace(Placeholder.BATCH_DATE.value, batch_date) \
                                .replace(Placeholder.LOG_STATUS.value, status) \
                                .replace(Placeholder.LOG_MSG.value, f'"{error_message}"' if error_message else "NULL")

    # Executes the sql statement
    bigquery.execute_query(reference_log_query)
    logger.info("counter.reference_log_update() function exected successfully")


def checkpoint_log_insert(process_id: int, batch_date:str, checkpoint_sequence: str, bigquery: Bigquery, logger: Logger) -> None:

    """Function which inserts an entry in the Checkpoint log table"""

    logger.info("counter.checkpoint_log_insert() function getting executed...")

    # Preparing checkpoint sql select statement
    checkpoint_log_query: str = SqlStatements.CHK_LOG_INSERT_STATEMENT \
                                .replace(Placeholder.PROCESS_ID.value, process_id) \
                                .replace(Placeholder.BATCH_DATE.value, batch_date) \
                                .replace(Placeholder.CHK_SEQUENCE_NO.value, checkpoint_sequence) \

    # Executes the sql statement
    bigquery.execute_query(checkpoint_log_query)

    logger.info("counter.checkpoint_log_insert() function executed successfully")


def checkpoint_log_update(process_id: int, checkpoint_sequence: str, status: str, log_message: dict, bigquery: Bigquery, logger: Logger) -> None:

    """Function which updates last entry in the Checkpoint log table"""

    logger.info("counter.checkpoint_log_update() function getting executed...")

    # Preparing checkpoint sql select statement
    checkpoint_log_query: str = SqlStatements.CHK_LOG_UPDATE_STATEMENT \
                                .replace(Placeholder.PROCESS_ID.value, process_id) \
                                .replace(Placeholder.CHK_SEQUENCE_NO.value, checkpoint_sequence) \
                                .replace(Placeholder.LOG_STATUS.value, status) \
                                .replace(Placeholder.LOG_MSG.value, f'JSON \'{json.dumps(log_message)}\'' if log_message else "NULL")

    # Executes the sql statement
    bigquery.execute_query(checkpoint_log_query)

    logger.info("counter.checkpoint_log_update() function executed successfully")