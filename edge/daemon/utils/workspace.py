# Standard Imports
import shutil
from pathlib import Path
# Third Party Imports
# Local Imports

class WorkspaceManager:
    """
    Sandbox Manager and Path Registry for abstracting file paths.
    """
    def __init__(self, root_path: str):
        self.root = Path(root_path)
    
    def cleanup(self) -> None:
        if self.root.exists(): 
            shutil.rmtree(self.root)

    def initialize(self) -> None:
        self.cleanup()
        self.root.mkdir(parents=True, exist_ok=True)

    def get_path_root(self) -> Path:
        return self.root

    def get_path_log(self) -> Path:
        return self.root / "log.txt"

    def get_path_download_archive_path(self) -> Path:
        return self.root / "package.zip"

    def get_path_download_archive_extracted(self) -> Path:
        return self.root/ "package"

    def get_path_bitstream(self) -> Path:
        return self.get_path_download_archive_extracted() / "design.bit"

    def get_path_hardwarehandoff(self) -> Path:
        return self.get_path_download_archive_extracted() / "design.hwh"

    def get_path_ambiguous_hil_test_executor(self) -> Path:
        return self.get_path_download_archive_extracted() / "hil_test.py"

    def get_path_additional_test_payloads_directory(self) -> Path:
        return self.get_path_download_archive_extracted() / "additional_payloads"

    def get_path_additional_test_artifacts(self) -> Path:
        (self.root / "additional_artifacts").mkdir(parents=True, exist_ok=True)
        return self.root / "additional_artifacts"
    
    def get_path_test_result_zip_archive(self) -> Path:
        return self.root / "test_result.zip"