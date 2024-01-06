from argparse import ArgumentParser, Namespace
from com.platform.utilities.logger import Logger
from com.platform.models.input_arguments import InputArguments


# Pass input arguments
import os, sys
sys.argv = [os.path.basename(__file__), "-id", "1000", "-batch", "  2023-12-24", "-from", "1", "-to", "10"]


class Inputs():

    """Class which get, parse, and validate user input arguments"""

    def __init__(self, logger: Logger):
        
        # Get, Parse, and Validate input arguments
        parser: ArgumentParser = ArgumentParser()

        parser.add_argument("-id",    "--process_id",      required=True,  help="Looks for the specific process id for execution")
        parser.add_argument("-batch", "--batch_date",      required=True,  help="Uses the batch date for execution")
        parser.add_argument("-from",  "--from_checkpoint", required=False, help="Executes the process from mentioned checkpoint", default=1)
        parser.add_argument("-to",    "--to_checkpoint",   required=False, help="Executes the process until to checkpoint", default=None)

        input_args: Namespace             = parser.parse_args()
        self.__parse_args: InputArguments = InputArguments(**vars(input_args))

        logger.title("Input Arguments")
        logger.info("Raw arguments: {}".format(input_args))
        logger.info("Parsed arguments: {}".format(self.__parse_args))

    def get(self):

        """Function helps in retrieving parsed arguments which is private to the class."""

        return self.__parse_args