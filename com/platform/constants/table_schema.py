from enum import Enum, unique


@unique
class CheckpointType(Enum):

    """Enum which defines the different checkpoint type"""

    SQL_EXECUTION: str = "SQL_EXECUTION"


@unique
class CheckpointScriptType(Enum):

    """Enum which defines the different script type"""

    FILE: str = "FILE"
    QUERY: str = "QUERY"
    

@unique
class LogStatus(Enum):

    """Enum which defines the diferent log status"""

    PROGRESS: str  = "In-Progress"
    COMPLETED: str = "Completed"
    FAILED: str    = "Failed"
    STOPPED: str   = "Stopped"