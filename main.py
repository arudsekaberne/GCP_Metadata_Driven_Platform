from dotenv import dotenv_values
from argparse import ArgumentParser, Namespace
from com.platform.models.input_arguments import InputArguments

# Pass input arguments
import os, sys
sys.argv = [os.path.basename(__file__), "-id", "1000", "-batch", "  2023-12-24", "-from", "2", "-to", "5", "-env", "Prod"]


# Get, Parse, and Validate input arguments
parser: ArgumentParser = ArgumentParser()

parser.add_argument("-id",    "--process_id",      required=True,  help="Looks for the specific process id for execution")
parser.add_argument("-batch", "--batch_date",      required=True,  help="Uses the batch date for execution")
parser.add_argument("-from",  "--from_checkpoint", required=False, help="Executes the process from mentioned checkpoint", default=1)
parser.add_argument("-to",    "--to_checkpoint",   required=False, help="Executes the process until to checkpoint", default=-1)
parser.add_argument("-env",   "--environment",     required=False, help="Determines the reference table `project id`", default="Test")

input_args: Namespace      = parser.parse_args()
parse_args: InputArguments = InputArguments(**vars(input_args))

print(parse_args)


# Get environmental variables
env_variables: dict = dotenv_values(".env")

