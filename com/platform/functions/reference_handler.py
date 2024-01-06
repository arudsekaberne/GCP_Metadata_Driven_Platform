from typing import List
from google.cloud.bigquery import Row
from com.platform.utilities.logger import Logger
from com.platform.utilities.bigquery import Bigquery
from google.api_core.exceptions import GoogleAPIError
from com.platform.constants.placeholders import Placeholder
from com.platform.models.reference_model import ReferenceModel
from com.platform.constants.sql_statements import SqlStatements
from com.platform.constants.common_variables import CommonVariables



def reference_handler(process_id: int, bigquery: Bigquery, logger: Logger) -> ReferenceModel:

    """Function which handles the entire reference tabe data"""

    logger.subtitle("Reference Handler")

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

    return parse_reference

    