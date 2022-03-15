from enum import Enum, unique


@unique
class TaskStatus(Enum):
    DRAFT = 1
    IN_PROGRESS = 2
    COMPLETED = 3
    ARCHIVED = 4


@unique
class TaskPriority(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
