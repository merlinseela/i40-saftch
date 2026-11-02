"""
Context Board to share information between states.
"""
# Standard Imports
# Third Party Imports
from dotenv import dotenv_values
# Local Imports
from utils.logger import LogAggregator
from utils.workspace import WorkspaceManager
from utils.api_client import APIClient

class JobContext:
    """
    Custom Data Class to house and share information across states.
    """
    def __init__(self):
        # Bootstrapping Environment Values and Core/Utility Classes
        self.daemon_environment: dict = dotenv_values(".env")
        self.workspace: WorkspaceManager = WorkspaceManager(self.
        daemon_environment["WORKSPACE_DIR"])
        self.logger: LogAggregator = LogAggregator(self.workspace.get_path_log())
        self.api_client: APIClient = APIClient(
            self.daemon_environment["API_BASE_URL"], 
            self.daemon_environment["M2M_TOKEN"], 
            self.daemon_environment["REST_REQUEST_TIMEOUT"]
            )
        # Job values
        self.board_id: str = self.daemon_environment["BOARD_NAME"]
        self.current_job_id: str = ""