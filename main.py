# Module imports

import os, sys
import atexit, signal
from glob import glob
from typing import List
from dotenv import dotenv_values
from com.platform.utilities.helper import Helper
from com.platform.utilities.logger import Logger
from com.platform.utilities.inputs import Inputs
from com.platform.utilities.storage import Storage
from com.platform.utilities.bigquery import Bigquery
from com.platform.models.input_model import InputModel
from com.platform.constants.table_schema import LogStatus
from com.platform.constants.placeholders import Placeholder
from com.platform.models.reference_model import ReferenceModel
from com.platform.models.checkpoint_model import CheckpointModel
from com.platform.constants.common_variables import CommonVariables
from com.platform.functions import cleaner, counter, runner, inspector, collector


# Pre-defined Functions

def interrupt_handler(signum, frame):
    
    """Function which handles manual interruption, eg: Quit run"""

    log_file_pattern: str = os.path.join(os.getcwd(), Helper.format_log_name(input_id, "*"))
    log_files: list       = glob(log_file_pattern)

    # Get last modified log file
    if len(log_files) > 0:
        log_file: str = sorted(log_files, key=os.path.getmtime, reverse=True)[0]

    logger: Logger = Logger(file_path=log_file)

    logger.title("Interrupt Handling")
    logger.info("Picked log file: {}".format(log_file))
    logger.warning("Execution got interrupted.")
    logger.warning("Therefore, the main and checkpoint log table 'INPROGRESS' value will gets updated with status 'STOPPED'.")

    # Update reference log with 'STOPPED' status
    if "main_log_insert" in globals():

        logger.info(f"Updating {CommonVariables.REF_LOG_TABLE_NAME} with status '{LogStatus.STOPPED.value}'")

        counter.main_log_update(parse_reference.process_id, LogStatus.STOPPED.value, "Execution got interrupted", bigquery, logger)


    # Ensure the exit functions are executed
    atexit._run_exitfuncs()
    sys.exit(2)
    

if __name__ == "__main__":

    # Fetch defined environmental variables
    env_variables: dict  = dotenv_values(".env")

    # Initialize logger
    input_id: int  = InputModel.validate_id(sys.argv[2])
    log_file: str  = os.path.join(os.getcwd(), Helper.format_log_name(input_id, CommonVariables.RUNTIME))
    logger: Logger = Logger(file_path=log_file)

    logger.title("Platform Execution")

    # Set service key to environment
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = env_variables.get("GCP_SERVICE_KEY_PATH")
    logger.info("GCP service key path set to environment")
    
    # Create google cloud clients
    storage: Storage = Storage(logger)
    bigquery: Bigquery = Bigquery(logger)
    logger.info("GCP API clients got created")

    try:

        logger.info("Plaform script started...")

        logger.info("Log file: {}".format(log_file))

        # Register interrupt handler
        signal.signal(signal.SIGINT, interrupt_handler)
        logger.info("Interrupt handler got registered")

        # Get, Parse, and Validate input arguments
        parse_args: InputModel = Inputs(logger).get()

        # Fetch, Parse, and Validate reference data
        parse_reference: ReferenceModel = collector.get_reference_data(parse_args.process_id, bigquery, logger)

        # Check all mandatory dir exists in GCS
        mandatory_folder = inspector.check_process_mandatory_folders(parse_reference.project_folder, storage, logger)

        # Check the current process is active
        inspector.is_process_active(parse_reference.is_active, parse_reference.process_name, logger)
        
        # Insert an entry in the main log
        main_log_insert = counter.main_log_insert(parse_reference.process_id, bigquery, logger)

        # Fetch, Parse, and Validate checkpoint data
        checkpoints: List[CheckpointModel] = collector.get_checkpoint_data(parse_reference.process_id, bigquery, logger)

        # Execute each checkpoint
        for checkpoint in checkpoints:
            runner.execute_checkpoint(parse_reference, checkpoint, bigquery, storage, logger)

        # Update reference log with 'COMPLETED' status
        counter.main_log_update(parse_reference.process_id, LogStatus.COMPLETED.value, None, bigquery, logger)

    except Exception as error:
        logger.title("Exception Block")

        # Update reference log with 'FAILED' status
        if "main_log_insert" in locals():

            logger.info(f"Updating {CommonVariables.REF_LOG_TABLE_NAME} with status '{LogStatus.FAILED.value}'")

            counter.main_log_update(parse_reference.process_id, LogStatus.FAILED.value, error.message.split("\n")[0].strip(), bigquery, logger)

        logger.error(error)
        logger.error("Main execution failed.")
        sys.exit(1)

    finally:
        logger.title("Final Block")
        
        if "mandatory_folder" in locals():

            # Uploads current log file in user project log folder
            storage.upload_file(log_file, f"{parse_reference.project_folder}/{CommonVariables.GCP_LOG_DIR_NAME}")
        
            # Clean log folder
            cleaner.clean_log_folder(parse_reference.process_id, parse_reference.project_folder, parse_reference.log_retention_count, storage, logger)

            # Removes existing log and maintain one
            log_file_path: str    = os.getcwd()
            log_file_name: str    = Placeholder.LOG_FILE_NAME.value.replace(Placeholder.PROCESS_ID.value, "*")
            log_file_name: str    = log_file_name.replace(Placeholder.RUNTIME.value, "*")
            log_file_pattern: str = os.path.join(log_file_path, log_file_name)
            log_files: list       = glob(log_file_pattern)

            if len(log_files) > 1:
                latest_log_file: str = sorted(log_files, key=os.path.getmtime, reverse=True)[0]

                for log_file in log_files:
                    if latest_log_file != log_file:
                        os.remove(log_file)
