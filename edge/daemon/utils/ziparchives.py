"""
Simple Zip-Archive methods.
"""
# Standard Library Imports
import zipfile
from pathlib import Path
from typing import List
# Third-Party Library Imports
# Local Imports

def unpack(zip_path: Path, extract_to: Path) -> None:
    """
    Unpacks a zip file into a target directory.
    """
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)

def pack(target_zip_path: Path, files_to_pack: List[Path]) -> None:
    """
    Packs a specific list of files into a target zip archive.
    """
    with zipfile.ZipFile(target_zip_path, "w") as zip_ref:
        for file_path in files_to_pack:
            zip_ref.write(file_path, arcname=file_path.name)