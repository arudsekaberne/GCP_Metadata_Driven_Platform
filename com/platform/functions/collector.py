from typing import Any, Dict, List
from google.cloud.bigquery import Row
from com.platform.utilities.logger import Logger
from com.platform.utilities.bigquery import Bigquery
from google.api_core.exceptions import GoogleAPIError
from com.platform.constants.placeholders import Placeholder
from com.platform.models.reference_model import ReferenceModel
from com.platform.constants.sql_statements import SqlStatements
from com.platform.models.checkpoint_model import CheckpointModel
from com.platform.constants.common_variables import CommonVariables



def get_reference_data(process_id: int, bigquery: Bigquery, logger: Logger) -> ReferenceModel:

    """Function which fetch, parse, and validate reference table data"""

    logger.title("Reference Execution")

    # Preparing reference sql select statement
    reference_query: str = SqlStatements.REF_SELECT_STATEMENT.replace(Placeholder.PROCESS_ID.value, process_id)

    # Executes the sql statement
    reference_query_result: List[Row] = bigquery.select_query(reference_query)

    # Raise exception if no output
    if len(reference_query_result) == 0:
        raise GoogleAPIError(f"There is no ID: {process_id} found under the reference table `{CommonVariables.REF_TABLE_NAME}`.")
    
    else:

        # Parse query output
        reference_query_result_dict = {key: value for key, value in reference_query_result[0].items()}
        parse_reference: ReferenceModel = ReferenceModel(**reference_query_result_dict)

        logger.info(f"Raw reference: {reference_query_result_dict}")
        logger.info(f"Parsed reference: {parse_reference}")

    logger.info(f"collector.get_reference_data() executed successfully, guarantee to get success and failure mail with log file as attachment")
    
    return parse_reference


def get_checkpoint_data(process_id: int, start_sequence: str, end_sequence: str, bigquery: Bigquery, logger: Logger) -> List[CheckpointModel]:

    """Function which fetch, parse, and validate ceckpoint table data"""

    logger.title("Checkpoint Execution")

    checkpoints: List[CheckpointModel] = []

    # Preparing reference sql select statement
    checkpoint_query: str = SqlStatements.CHK_SELECT_STATEMENT \
                                .replace(Placeholder.PROCESS_ID.value, process_id) \
                                .replace(Placeholder.START_SEQUENCE.value, start_sequence)
    
    checkpoint_query: str = checkpoint_query.replace(Placeholder.END_SEQUENCE.value,
                                                     f"checkpoint_sequence <= {end_sequence} AND" if end_sequence else "")

    # Executes the sql statement
    checkpoint_query_result: List[Row] = bigquery.select_query(checkpoint_query)

    # Raise exception if no output
    if len(checkpoint_query_result) == 0:
        raise GoogleAPIError(f"There are no checkpoints active or registered in `{CommonVariables.REF_TABLE_NAME}` under process id: {process_id}.")
    
    else:

        # Parse query output
        for checkpoint in checkpoint_query_result:

            checkpoint_dict: Dict[str, Any] = {key: value for key, value in checkpoint.items()}

            parse_checkpoint: CheckpointModel = CheckpointModel(**checkpoint_dict)
            checkpoints.append(parse_checkpoint)

            logger.info(f"Raw checkpoint: {checkpoint_dict}")
            logger.info(f"Parsed checkpoint: {parse_checkpoint}")

    logger.info(f"collector.get_checkpoint_data() executed successfully")
    
    return checkpoints

