from enum import Enum, unique


@unique
class Placeholder(Enum):

    PROCESS_ID: str    = r"${ID}"
    RUNTIME: str       = r"${RUNTIME}"
    LOG_FILE_NAME: str = fr"{PROCESS_ID}_PLATFORM_{RUNTIME}.log"