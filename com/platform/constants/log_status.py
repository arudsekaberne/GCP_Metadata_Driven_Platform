from enum import Enum, unique


@unique
class LogStatus(Enum):

    PROGRESS: str  = "PROGRESS"
    COMPLETED: str = "COMPLETED"
    FAILED: str    = "FAILED"
    STOPPED: str   = "STOPPED"

    