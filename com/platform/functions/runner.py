from com.platform.utilities.logger import Logger
from com.platform.utilities.storage import Storage
from com.platform.utilities.bigquery import Bigquery
from com.platform.models.reference_model import ReferenceModel
from com.platform.models.checkpoint_model import CheckpointModel
from com.platform.constants.table_schema import CheckpointType, CheckpointScriptType


def sql_execution(parse_reference: ReferenceModel, checkpoint: CheckpointModel, bigquery: Bigquery, storage: Storage, logger: Logger):
    
    """Function which handles SQL_EXECUTION checkpoint"""
    
    logger.info("runner.sql_execution() function getting executed...")

    logger.info(f"Script type: {checkpoint.script_type}")

    if checkpoint.script_type == CheckpointScriptType.QUERY.value:
        bigquery.execute_query(checkpoint.script)

    elif checkpoint.script_type == CheckpointScriptType.FILE.value:
        bigquery.execute_file(parse_reference.project_folder, checkpoint.script, storage)
        
    logger.info("runner.sql_execution() function executed successfully")


def execute_checkpoint(parse_reference: ReferenceModel, checkpoint: CheckpointModel, bigquery: Bigquery, storage: Storage, logger: Logger):

    """Function which map checkpoint type with respective function and execute"""

    CHECKPOINT_AND_FUNCTION = {
        CheckpointType.SQL_EXECUTION.value: sql_execution
    }

    logger.title(f"Checkpoint: {checkpoint.checkpoint_sequence} - {checkpoint.checkpoint_type}")

    # Actual Exectioner
    CHECKPOINT_AND_FUNCTION[checkpoint.checkpoint_type](parse_reference, checkpoint, bigquery, storage, logger)



