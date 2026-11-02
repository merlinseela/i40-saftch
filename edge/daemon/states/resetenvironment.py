# Standard Library Imports
import traceback
# Third-Party Library Imports
# Local Imports
from core.context import JobContext
from core.enums import Status
from states.base import BaseState

class ResetEnvironmentState(BaseState):
    def execute(self, context: JobContext) -> Status:
        print(f"[I40-SAFTCH-DAEMON] Initiating teardown for Job: {context.current_job_id}...")
        context.logger.info("[STATE: TEARDOWN] Wiping workspace and resetting hardware...")
        context.logger.info("Closing logs for current job.")
        
        try:
            # Future V0.2.0 Hardware Reset Hook
            # Overlay("/path/to/dummy_bitstream.bit").download()
            # print("[I40-SAFTCH-DAEMON] FPGA Fabric wiped! Dummy-Bitstream overwrite successful")

            context.workspace.cleanup()
            print("[I40-SAFTCH-DAEMON] Workspace directory successfully deleted.")
            print("[I40-SAFTCH-DAEMON] Teardown complete. Ready for next job.")
            return Status.SUCCESS

        except Exception as e:
            print(f"[I40-SAFTCH-DAEMON] FATAL ERROR during teardown: {e}")
            print(traceback.format_exc())
            return Status.FAIL