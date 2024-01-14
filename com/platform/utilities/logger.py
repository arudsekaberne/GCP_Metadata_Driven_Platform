import logging


class Logger():

    """Class which helps in modularizing logging method"""

    __BANNER_LEN: int = 100

    def __init__(self, file_path: str, filemode: str = "a"):

        # Create and configure logger
        logging.basicConfig(filename=file_path, format="%(asctime)s :: %(levelname)-8s :: %(message)s", filemode=filemode)

        # Creating an object
        self.__log: Logger = logging.getLogger()

        # Setting the threshold of logger to DEBUG
        self.__log.setLevel(logging.INFO)


    def debug(self, value: str):
        self.__log.debug(value); print(f"DEBUG :: {value}")

    def info(self, value: str):
        self.__log.info(value); print(f"INFO :: {value}")

    def warning(self, value: str):
        self.__log.warning(value); print(f"WARN :: {value}")

    def error(self, value: str):
        self.__log.error(value); print(f"ERROR :: {value}")

    def critical(self, value: str):
        self.__log.critical(value); print(f"CRITICAL :: {value}")


    # Create a title card
    def title(self, value: str):
        title_dec: str = "*" * Logger.__BANNER_LEN
        title_str: str = f"\n{title_dec}\n{value.strip().center(Logger.__BANNER_LEN, ' ')}\n{title_dec}"
        self.__log.info(title_str); print(title_str)


    # Create a sub title card
    def subtitle(self, value: str):
        sub_title_str = f" {value.strip()} "
        sub_title_str: str = f"\n{sub_title_str.center(Logger.__BANNER_LEN, '-')}" 
        self.__log.info(sub_title_str); print(sub_title_str)

    
 