# Standard Imports
import time
from pathlib import Path
from enum import Enum
# Third Party Imports
# Local Imports

class LogLevel(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class LogAggregator:
    """
    Streams log messages to a log file.
    """
    
    def __init__(self, log_file_path: Path):
        self.log_file_path = log_file_path
        self.log_file_path.parent.mkdir(parents=True, exist_ok=True)

    def _write(self, level: LogLevel, message: str):
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        formatted_msg = f"[{timestamp}] - [{level.value}] - {message}\n"
        
        with open(self.log_file_path, "a") as f:
            f.write(formatted_msg)

    def info(self, message: str) -> None:
        self._write(LogLevel.INFO, message)

    def warning(self, message: str) -> None:
        self._write(LogLevel.WARNING, message)

    def error(self, message: str) -> None:
        self._write(LogLevel.ERROR, message)