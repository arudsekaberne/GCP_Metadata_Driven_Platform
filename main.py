import os, sys
import atexit, signal
from glob import glob
from datetime import datetime
from dotenv import dotenv_values
from com.platform.utilities.logger import Logger
from com.platform.utilities.inputs import Inputs
from com.platform.models.input_arguments import InputArguments


# Pre-defined variable
raw_id: str       = int(sys.argv[2].strip())
runtime: str      = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file_ptn: str = "./log/{}_platform_*.log".format(raw_id)
log_file: str     = log_file_ptn.replace("*", runtime)


# Functions

def interrupt_handler(signum, frame):

    """Function which handles manual interruption, eg: Quit run"""

    log_files: list = glob(log_file_ptn)

    # Get last modified log file
    if len(log_files) > 0:
        log_file: str = sorted(log_files, key=os.path.getmtime, reverse=True)[0]

    logger: Logger = Logger(file_path=log_file, filemode="a")
    logger.title("Interrupt Handling")
    logger.info("Selected log file: {}".format(log_file))
    logger.warning("Execution got manually interrupted.")
    logger.warning("Therefore, the main and checkpoint log table value will gets updated with status 'STOPPED'.")

    # Ensure the exit functions are executed
    atexit._run_exitfuncs()
    sys.exit(1)


def main_execution():

    logger.info("Main execution started...")

    # Get defined environmental variables
    env_variables: dict = dotenv_values(".env")
    logger.info(".env file values got loaded")


    # Set service key to environment
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = env_variables.get("GCP_SERVICE_KEY_PATH")
    logger.info("GCP service key path set to environment")


    # Get, Parse, and Validate input arguments
    parse_args: InputArguments = Inputs(logger).get()  

    while True:
        pass

if __name__ == "__main__":

    try:
        
        # Initialize logger
        logger: Logger = Logger(file_path=log_file)

        # Register interrupt handler
        signal.signal(signal.SIGINT, interrupt_handler)
    
        # Main execution
        main_execution()
        
    except Exception as error:
        logger.error("Main execution failed...")
        logger.error(error)

