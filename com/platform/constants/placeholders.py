from enum import Enum, unique


@unique
class Placeholder(Enum):

    PROCESS_ID: str        = r"${ID}"
    RUNTIME: str           = r"${RUNTIME}"
    BATCH_DATE: str        = r"${BATCH_DATE}"
    LOG_STATUS: str        = r"${LOG_STATUS}"
    CURRENT_DATE: str      = r"${CURRENT_DATE}"
    LOG_ERROR_MSG: str     = r"${LOG_ERROR_MSG}"
    CURRENT_TIMESTAMP: str = r"${CURRENT_TIMESTAMP}"
    LOG_FILE_NAME: str     = fr"{PROCESS_ID}_PLATFORM_{RUNTIME}.log"