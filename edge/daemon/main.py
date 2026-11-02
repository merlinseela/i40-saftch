"""
Main class/script of the i40-saftch EdgeDaemon.
"""
# Standard Library Imports
import sys
import time
# Third Party Imports
from dotenv import dotenv_values
# Local Imports
from core.context import JobContext
from core.enums import Status
from states.polljobs import PollJobsState
from states.initializeenvironment import InitializeEnvironmentState
from states.downloadunpack import DownloadUnpackState
from states.testexecution import TestExecutionState
from states.packupload import PackUploadState
from states.resetenvironment import ResetEnvironmentState

class EdgeAgentDaemon:
    """
    Central mediator routing workflow.
    """
    def __init__(self):
        """
        Initializes the Daemon, its necessary base Objects and houses the routing table for the state machine.
        """
        # Bootstrapping
        self.job_context: JobContext = None
        
        # Routing Table: Maps (CurrentStateClass, StatusReturned) -> NextStateClass
        self.routing_table = {
            # PollJobsState
            (PollJobsState, Status.SUCCESS): InitializeEnvironmentState,
            (PollJobsState, Status.NO_JOB): PollJobsState,
            (PollJobsState, Status.FAIL): PollJobsState,
            
            # InitializeEnvironment
            (InitializeEnvironmentState, Status.SUCCESS): DownloadUnpackState,
            # Note: Usually you want another State here, however if anything goes wrong while preparing the Environment for the HiL-Test, the Daemon should crash completely.
            # This is an extreme edge case that points to problems outside the scope of this framework, like RAM-Overflow, broken SD-Card or other critical failures. Check run() below for more context.

            # DownloadUnpackState
            (DownloadUnpackState, Status.SUCCESS): TestExecutionState,
            (DownloadUnpackState, Status.FAIL): PackUploadState,
            
            # TestExecutionState
            (TestExecutionState, Status.SUCCESS): PackUploadState,
            (TestExecutionState, Status.FAIL): PackUploadState,
            
            # PackUploadState
            (PackUploadState, Status.SUCCESS): ResetEnvironmentState,
            (PackUploadState, Status.RETRY): PackUploadState,
            (PackUploadState, Status.FAIL): ResetEnvironmentState,
            
            # ResetEnvironmentState
            (ResetEnvironmentState, Status.SUCCESS): PollJobsState,
            # Note: Why no second state? -> Same as InitializeEnvironmentState...
        }

        # Seed first state
        self.current_state = PollJobsState()

    def run(self):
        print("[I40-SAFTCH-DAEMON] Starting I40-SAFTCH DAEMON!")
        while True:
            if isinstance(self.current_state, PollJobsState):
                print("[I40-SAFTCH-DAEMON] Creating fresh Job Context!")
                self.job_context = JobContext()

            print(f"[I40-SAFTCH-DAEMON] Executing state: {type(self.current_state).__name__}!")
            status = self.current_state.execute(self.job_context)
            
            try:
                next_state_class = self.routing_table[(type(self.current_state), status)]
                self.current_state = next_state_class()
            except KeyError:
                print(f"\n[FATAL ERROR] State Machine halted. No route defined for {type(self.current_state).__name__} returning {status.name}.")
                print("[FATAL ERROR] Indicates critical hardware or OS-level failure! (e.g. RAM Overflow). Terminating zombie-daemon!")
                sys.exit(1)

if __name__ == "__main__":
    daemon = EdgeAgentDaemon()
    try:
        daemon.run()
    except KeyboardInterrupt:
        print("\n[I40-SAFTCH-DAEMON] Shutting down gracefully...")