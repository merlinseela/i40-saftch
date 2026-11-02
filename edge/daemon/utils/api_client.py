# Standard Imports
from pathlib import Path
# Third Party Imports
import requests
# Local Imports

class APIClient:
    def __init__(self, base_url: str, token: str, timeout: str):
        self.base_url = base_url
        self.base_header = {"Authorization": f"Bearer {token}"}
        self.timeout = int(timeout)
        
    def get_next_job_id(self) -> str:
        endpoint_get_next_job_id = f"{self.base_url}/jobs/next"
        response = requests.get(
            endpoint_get_next_job_id,
            headers=self.base_header,
            timeout=self.timeout
        )       
        response.raise_for_status()
        job_id_dict = response.json() 
        return job_id_dict.get("job_id")

    def get_next_job_artifacts(self, job_id: str, destination_path: Path) -> None:
        endpoint_get_job_artifacts = f"{self.base_url}/jobs/{job_id}/artifacts"
        with requests.get(endpoint_get_job_artifacts, headers=self.base_header, stream=True, timeout=self.timeout) as response:
            response.raise_for_status()
            with open(destination_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        
    def upload_job_results(self, job_id: str, zip_path: Path) -> None:
        endpoint = f"{self.base_url}/jobs/{job_id}/result"
        with open(zip_path, "rb") as f:
            response = requests.post(
                endpoint,
                headers=self.base_header,
                files={"file": ("results.zip", f, "application/zip")},
                timeout=self.timeout
            )
            response.raise_for_status()