from enum import Enum


class TypeMessage(Enum):
    """
    Enum to represent the different types of messages for responses.

    Attributes
    ----------
    INFO : int
        Represents an informational message.
    WARNING : int
        Represents a warning message.
    ERROR : int
        Represents an error message.
    """

    INFO = 1
    WARNING = 2
    ERROR = 3
