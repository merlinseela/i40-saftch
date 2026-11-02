"""
Abstract contract that all external Hardware-in-the-Loop tests must fulfill.
"""
# Standard Imports
from abc import ABC, abstractmethod
# Third Party Imports
# Local Imports
from core.context import JobContext

class HiLTestExecutor(ABC):
    @abstractmethod
    def execute(self, context: JobContext) -> None:
        pass