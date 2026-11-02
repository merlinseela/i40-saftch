"""
Abstract contract for states of the I40-SAFTCH Edge Daemon.
"""
# Standard Imports
from abc import ABC, abstractmethod
# Third Party Imports
# Local Imports
from core.context import JobContext
from core.enums import Status

class BaseState(ABC):
    @abstractmethod
    def execute(self, context: JobContext) -> Status:
        """Executes the isolated state logic and returns a routing Status."""
        pass