"""
Houses all enums the daemon has. Currently only state status resided here.
"""
# Standard Library Imports
from enum import Enum, auto
# Third Party Imports
# Local Imports

class Status(Enum):
    """
    Status a State can have.
    """
    SUCCESS = auto()
    FAIL = auto()
    NO_JOB = auto()
    RETRY = auto()
