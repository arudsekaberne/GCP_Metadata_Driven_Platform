from google.cloud.storage import Client
from com.platform.utilities.helper import Helper
from com.platform.utilities.logger import Logger


class Storage():

    """Class which handles all cloud storage executions"""

    def __init__(self, logger: Logger):
        self.logger: Logger = logger
        self.client: Client = Client()
        self.logger.info("Cloud storage client got created")