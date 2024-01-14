from enum import Enum, unique


@unique
class CheckpointType(Enum):

    SQL_EXECUTION: str = "SQL_EXECUTION"
    