from com.platform.functions import counter
from com.platform.models.input_model import InputModel
from com.platform.utilities.logger import Logger
from com.platform.utilities.storage import Storage
from com.platform.utilities.bigquery import Bigquery
from com.platform.models.reference_model import ReferenceModel
from com.platform.models.checkpoint_model import CheckpointModel
from com.platform.constants.table_schema import CheckpointType, CheckpointScriptType, LogStatus


def sql_execution(project_folder: str, script_type: str, script: str, bigquery: Bigquery, storage: Storage, logger: Logger):
    
    """Function which handles SQL_EXECUTION checkpoint"""
    
    logger.info("runner.sql_execution() function getting executed...")

    logger.info(f"Script type: {script_type}")

    if script_type == CheckpointScriptType.QUERY.value:
        bigquery.execute_query(script)

    elif script_type == CheckpointScriptType.FILE.value:
        bigquery.execute_file(project_folder, script, storage)
        
    logger.info("runner.sql_execution() function executed successfully")


def execute_checkpoint(parse_args: InputModel, parse_reference: ReferenceModel, checkpoint: CheckpointModel, bigquery: Bigquery, storage: Storage, logger: Logger):

    """Function which map checkpoint type with respective function and execute"""

    logger.title(f"Checkpoint: {checkpoint.checkpoint_sequence} - {checkpoint.checkpoint_type}")

    # Insert an entry in the checkpoint log
    counter.checkpoint_log_insert(parse_reference.process_id, parse_args.batch_date, checkpoint.checkpoint_sequence, bigquery, logger)

    try:
        # Actual Exectioner
        if checkpoint.checkpoint_type == CheckpointType.SQL_EXECUTION.value:
            sql_execution(parse_reference.project_folder, checkpoint.script_type, checkpoint.script, bigquery, storage, logger)

        # Can be sed to log different message
        log_message: dict = None
        counter.checkpoint_log_update(parse_reference.process_id, checkpoint.checkpoint_sequence, LogStatus.COMPLETED.value, log_message, bigquery, logger)

    except Exception as error:

        log_message: dict = {"error": error.message.split("\n")[0].strip().replace('"', '\\\"')}
        counter.checkpoint_log_update(parse_reference.process_id, checkpoint.checkpoint_sequence, LogStatus.FAILED.value, log_message, bigquery, logger)

        raise error
    
    