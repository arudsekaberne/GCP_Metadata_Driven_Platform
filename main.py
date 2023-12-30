import os, sys
import atexit, signal
from glob import glob
from dotenv import dotenv_values
from com.platform.utilities.logger import Logger
from com.platform.utilities.inputs import Inputs
from com.platform.models.input_arguments import InputArguments
from com.platform.models.static_variables import StaticVariables


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
    sys.exit(1)


def main_execution():

    logger.info("Main execution started...")

    # Get, Parse, and Validate input arguments
    parse_args: InputArguments = Inputs(logger).get()  

    while True:
        pass


if __name__ == "__main__":

    # Pre-defined common static variables
    static_variables: dict = StaticVariables.get_class_fields()

    # Fetch defined environmental variables
    env_variables: dict  = dotenv_values(".env")

    # Initialize logger
    input_id: int         = int(sys.argv[2].strip())
    log_file_path: str    = env_variables.get("LOG_FILE_PATH")
    log_file_name_ph: str = static_variables.get("LOG_FILE_NAME_PLACEHOLDER")
    log_file: str         = os.path.join(log_file_path, log_file_name_ph.format(input_id, static_variables.get("RUNTIME")))
    logger: Logger        = Logger(file_path=log_file)

    try:

        logger.title("Initial Setup")

        logger.info("Log file: {}".format(log_file))

        # Register interrupt handler
        signal.signal(signal.SIGINT, interrupt_handler)
        logger.info("Interrupt handler got registered")

        # Set service key to environment
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = env_variables.get("GCP_SERVICE_KEY_PATH")
        logger.info("GCP service key path set to environment")
    
        # Main execution
        main_execution()
        
    except Exception as error:
        logger.error("Main execution failed...")
        logger.error(error)

