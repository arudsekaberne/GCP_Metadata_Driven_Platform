import logging


class Logger():

    """Class which helps in modularizing logging method"""

    def __init__(self, file_path: str, filemode: str = "w"):

        # Create and configure logger
        logging.basicConfig(filename=file_path, format="%(asctime)s :: %(levelname)-8s :: %(message)s", filemode=filemode)

        # Creating an object
        self.__log: Logger = logging.getLogger()

        # Setting the threshold of logger to DEBUG
        self.__log.setLevel(logging.INFO)


    def debug(self, value: str):
        self.__log.debug(value); print("DEBUG :: {}".format(value))

    def info(self, value: str):
        self.__log.info(value); print("INFO :: {}".format(value))

    def warning(self, value: str):
        self.__log.warning(value); print("WARN :: {}".format(value))

    def error(self, value: str):
        self.__log.error(value); print("ERROR :: {}".format(value))

    def critical(self, value: str):
        self.__log.critical(value); print("CRITICAL :: {}".format(value))

    # Create a title card
    def title(self, value: str):
        title_len: int = 75
        title_dec: str = "*" * title_len
        title_str: str = "\n{0}\n{1}\n{0}".format(title_dec, value.center(title_len, " "))
        self.__log.info(title_str); print(title_str)

    
 