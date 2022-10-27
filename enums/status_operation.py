from enum import Enum


class STATUS_OPERATION(Enum):
    CREATE = 1
    COMMIT = 2
    ERROR = 3
    REJECT = 4
