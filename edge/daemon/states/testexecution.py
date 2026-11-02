# Standard Library Imports
import importlib.util
import traceback
# Third-Party Library Imports
# Local Imports
from core.context import JobContext
from core.enums import Status
from states.base import BaseState

class TestExecutionState(BaseState):
    def execute(self, context: JobContext) -> Status:
        print(f"[I40-SAFTCH-DAEMON] Starting execution of job: {context.current_job_id}...")
        try:
            spec = importlib.util.spec_from_file_location(
                "ambiguous_hil_test_executor",
                context.workspace.get_path_ambiguous_hil_test_executor()
                )
            test_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(test_module)
            executor = getattr(test_module, "hil_test")()
            executor.execute(context)
            print("[I40-SAFTCH-DAEMON] Test execution completed successfully.")
            return Status.SUCCESS
        
        except Exception as e:
            print(f"[I40-SAFTCH-DAEMON] Test execution failed: {e}")
            context.logger.error(f"Test Execution Failed: {e}")
            context.logger.error(traceback.format_exc())
            return Status.FAIL