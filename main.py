import os
from dotenv import dotenv_values
from com.platform.utilities.logger import Logger
from com.platform.utilities.inputs import Inputs
from com.platform.models.input_arguments import InputArguments

# Initialize logger
logger: Logger = Logger(file_path="./logger.log")
logger.info("Platform execution started...")


# Get environmental variables
env_variables: dict = dotenv_values(".env")
logger.info(".env file values got loaded")


# Set service key to environment
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = env_variables.get("GCP_SERVICE_KEY_PATH")
logger.info("Google application credential got set to environment")


# Get, Parse, and Validate input arguments
parse_args: InputArguments = Inputs(logger).get()