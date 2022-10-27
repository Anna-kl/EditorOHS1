from enum import Enum


class Status(Enum):
    ACTIVE = 1
    CORRUPT = 2
    DELETE = 3
    ARCHIVE = 4
