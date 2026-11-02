# Standard Library Imports
import time
import traceback
# Third-Party Library Imports
# Local Imports
from core.context import JobContext
from core.enums import Status
from states.base import BaseState
from utils.ziparchives import pack

class PackUploadState(BaseState):
    def execute(self, context: JobContext) -> Status:
        print(f"[I40-SAFTCH-DAEMON] Zipping and uploading results for Job: {context.current_job_id}...")
        context.logger.info("Zipping and sending results...")
        try:
            files_to_pack = [context.workspace.get_path_log()]

            if context.workspace.get_path_additional_test_artifacts().exists():
                for item in context.workspace.get_path_additional_test_artifacts().rglob('*'):
                    if item.is_file():
                        files_to_pack.append(item)
                
            print("[I40-SAFTCH-DAEMON] Packing artifacts...")    
            pack(
                context.workspace.get_path_test_result_zip_archive(),
                files_to_pack
                )
            
            print("[I40-SAFTCH-DAEMON] Pushing test artifact archive to Server...")
            context.api_client.upload_job_results(
                context.current_job_id,
                context.workspace.get_path_test_result_zip_archive()
                )
            
            print("[I40-SAFTCH-DAEMON] Upload successful.")
            return Status.SUCCESS
            
        except Exception as e:
            print(f"[I40-SAFTCH-DAEMON] Upload failed: {e}. Retrying in {context.daemon_environment['REST_RETRY_TIME']} seconds...")
            context.logger.error(f"Upload failed: {e}. Retrying...")
            context.logger.error(traceback.format_exc())
            time.sleep(int(context.daemon_environment['REST_RETRY_TIME']))
            return Status.RETRY