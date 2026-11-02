# Standard Library Imports
import time
# Third-Party Library Imports
import requests
# Local Imports
from core.context import JobContext
from core.enums import Status
from states.base import BaseState

class PollJobsState(BaseState):
    """
    Job aka. HiL-test polling state.
    """
    def execute(self, context: JobContext) -> Status:
        print("[I40-SAFTCH-DAEMON] Polling available jobs...")
        try:
            job_id = context.api_client.get_next_job_id()
            if job_id:
                context.current_job_id = job_id
                print(f"[I40-SAFTCH-DAEMON] Job acquired! Job-ID: {context.current_job_id}")
                return Status.SUCCESS
            else:
                print(f"[I40-SAFTCH-DAEMON] No jobs available. Retrying in {context.daemon_environment['POLL_INTERVAL_SECONDS']} seconds...")
                time.sleep(int(context.daemon_environment['POLL_INTERVAL_SECONDS']))
                return Status.NO_JOB
                
        except requests.RequestException as e:
            print(f"[I40-SAFTCH-DAEMON] Network error during polling: {e}")
            print(f"[I40-SAFTCH-DAEMON] Retrying connection in {context.daemon_environment['REST_RETRY_TIME']} seconds...")
            time.sleep(int(context.daemon_environment['REST_RETRY_TIME']))
            return Status.FAIL