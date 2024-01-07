import logging


class Logger():

    """Class which helps in modularizing logging method"""

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
        title_len: int = 75
        title_dec: str = "*" * title_len
        title_str: str = f"\n{title_dec}\n{value.strip().title().center(title_len, ' ')}\n{title_dec}"
        self.__log.info(title_str); print(title_str)


    # Create a sub title card
    def subtitle(self, value: str):
        subtitle_len: int = 75
        sub_title_str = f" {value.strip().title()} "
        sub_title_str: str = f"\n{sub_title_str.center(subtitle_len, '-')}" 
        self.__log.info(sub_title_str); print(sub_title_str)

    
 