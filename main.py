import os, sys
import atexit, signal
from glob import glob
from dotenv import dotenv_values
from com.platform.utilities.logger import Logger
from com.platform.utilities.inputs import Inputs
from com.platform.utilities.storage import Storage
from com.platform.utilities.bigquery import Bigquery
from com.platform.models.input_model import InputModel
from com.platform.models.reference_model import ReferenceModel
from com.platform.functions.inspect_bucket import inspect_bucket
from com.platform.constants.common_variables import CommonVariables
from com.platform.functions.get_reference_data import get_reference_data


# Pre-defined Functions

def interrupt_handler(signum, frame):

    """Function which handles manual interruption, eg: Quit run"""

    log_file_pattern: str = os.path.join(log_file_path, log_file_name_ph.format(input_id, "*"))
    log_files: list       = glob(log_file_pattern)

    # Get last modified log file
    if len(log_files) > 0:
        log_file: str = sorted(log_files, key=os.path.getmtime, reverse=True)[0]

    logger: Logger = Logger(file_path=log_file, filemode="a")

    logger.title("Interrupt Handling")
    logger.info("Picked log file: {}".format(log_file))
    logger.warning("Execution got manually interrupted.")
    logger.warning("Therefore, the main and checkpoint log table value will gets updated with status 'STOPPED'.")

    # Ensure the exit functions are executed
    atexit._run_exitfuncs()
    sys.exit(2)
    

def main_execution():
    
    """Function which provides all necessary inputs to the main platform execution functions"""

    logger.title("Main Execution")

    # Set service key to environment
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = env_variables.get("GCP_SERVICE_KEY_PATH")
    logger.info("GCP service key path set to environment")
    
    # Create google cloud clients
    bigquery: Bigquery = Bigquery(logger)
    storage: Storage = Storage(logger)

    # Fetch, Parse, and Validate reference data
    parse_reference: ReferenceModel = get_reference_data(parse_args.process_id, bigquery, logger)

    # Check all mandatory dir exists in GCS
    inspect_bucket(parse_reference.project_folder, storage, logger)
     

if __name__ == "__main__":

    # Fetch defined environmental variables
    env_variables: dict  = dotenv_values(".env")

    # Initialize logger
    input_id: int         = InputModel.validate_id(sys.argv[2])
    log_file_path: str    = CommonVariables.LOG_FILE_PATH
    log_file_name_ph: str = CommonVariables.LOG_FILE_NAME_PLACEHOLDER
    log_file: str         = os.path.join(log_file_path, log_file_name_ph.format(input_id, CommonVariables.RUNTIME))
    logger: Logger        = Logger(file_path=log_file)

    try:

        logger.info("Plaform script started...")

        logger.info("Log file: {}".format(log_file))

        # Register interrupt handler
        signal.signal(signal.SIGINT, interrupt_handler)
        logger.info("Interrupt handler got registered")

        # Get, Parse, and Validate input arguments
        parse_args: InputModel = Inputs(logger).get()

        # Enterance for all platform execution
        main_execution()
        
    except Exception as error:
        
        logger.error(error)
        logger.error("Main execution failed.")
        sys.exit(1)

