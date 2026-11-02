# Standard Library Imports
import traceback
# Third-Party Library Imports
# Local Imports
from core.context import JobContext
from core.enums import Status
from states.base import BaseState
from utils.ziparchives import unpack

class DownloadUnpackState(BaseState):
    def execute(self, context: JobContext) -> Status:
        print("[I40-SAFTCH-DAEMON] Entering Download state...")
        context.logger.info(f"Attempting download of job Artifacts with job_id: {context.current_job_id}")
        
        try:
            context.api_client.get_next_job_artifacts(
                context.current_job_id,
                context.workspace.get_path_download_archive_path())
            
            print("[I40-SAFTCH-DAEMON] job Artifacts received! Attempting to unpack...")

            unpack(
                context.workspace.get_path_download_archive_path(),
                context.workspace.get_path_download_archive_extracted()
                )
            
            print("[I40-SAFTCH-DAEMON] Unpacking succeeded!")

            return Status.SUCCESS

        except Exception as e:
            print("[I40-SAFTCH-DAEMON] Download failed... Check Test_Logs for further information...")
            context.logger.error(f"Download/Unpack failed: {e}")
            context.logger.error(traceback.format_exc())
            return Status.FAIL