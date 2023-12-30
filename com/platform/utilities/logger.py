import logging



 

# logger.debug("Harmless debug Message")
# logger.info("Just an information")
# logger.warning("Its a Warning")
# logger.error("Did you try to divide by zero")
# logger.critical("Internet is down")


class Logger():

    def __init__(self, file_path: str):

        # Create and configure logger
        logging.basicConfig(filename=file_path, format="%(asctime)s %(message)s", filemode="w")

        # Creating an object
        self.__log: Logger = logging.getLogger()

        # Setting the threshold of logger to DEBUG
        self.__log.setLevel(logging.DEBUG)


    def debug(self, value: str):
        self.__log.debug(value); print(value)

    def info(self, value: str):
        self.__log.info(value); print(value)

    def warning(self, value: str):
        self.__log.warning(value); print(value)

    def error(self, value: str):
        self.__log.error(value); print(value)

    def critical(self, value: str):
        self.__log.critical(value); print(value)

    def title(self, value: str):
        title_len: int = 75
        title_dec: str = "*" * title_len
        title_str: str = "\n{0}\n{1}\n{0}".format(title_dec, value.center(title_len, " "))
        self.__log.info(title_str); print(title_str)

    
 