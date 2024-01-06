from enum import Enum, unique


@unique
class Placeholder(Enum):

    PROCESS_ID = r"${ID}"