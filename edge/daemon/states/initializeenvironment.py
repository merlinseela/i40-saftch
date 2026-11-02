# Standard Library Imports
import traceback
# Third-Party Library Imports
# Local Imports
from core.context import JobContext
from core.enums import Status
from states.base import BaseState
from utils.workspace import WorkspaceManager
from utils.logger import LogAggregator  # Adjust this import path to match your project structure

class InitializeEnvironmentState(BaseState):
    def execute(self, context: 'JobContext') -> 'Status':
        print(f"[I40-SAFTCH-DAEMON] Initializing physical environment for Job: {context.current_job_id}...")
        try:
            context.workspace.initialize()
            print(f"[I40-SAFTCH-DAEMON] Workspace mounted and wiped at {context.workspace.root}")
            
            # Since the Logger is created during JobContext Creation, this is just for verification that is actually works...
            context.logger.info(f"Environment initialization complete for Job: {context.current_job_id}")
            return Status.SUCCESS

        except Exception as e:
            print(f"[I40-SAFTCH-DAEMON] FATAL ERROR during environment initialization: {e}")
            print(traceback.format_exc())
            return Status.FAIL