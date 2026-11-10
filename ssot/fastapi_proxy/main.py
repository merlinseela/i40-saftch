# Standard Library Imports
from base64 import urlsafe_b64decode, urlsafe_b64encode
from contextlib import asynccontextmanager
from typing import Optional
from pathlib import Path
import shutil
import io
import os # leave in place when debugging starlette.BackgroundTask
import zipfile
from datetime import datetime
# Third Party Imports
from fastapi import FastAPI, Depends, Request, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from starlette.background import BackgroundTask
import uvicorn
import httpx
# Local Imports
from core.context import SSOTContext
from services.landing_page import get_landing_page
from routes.register_device import RegisterDeviceService
from routes.register_fpga_design import RegisterFpgaDesignService
from utils.m2m_check import m2m_check

# Bootstrapping
@asynccontextmanager
async def lifespan(app: FastAPI):
    ssot_context = SSOTContext()
    app.state.ssot_context = ssot_context
    # --- #
    yield     
    # --- #
    await app.state.ssot_context.basyxclient.close()

app = FastAPI(title="i40-SAFTCH", version="0.1.0", lifespan=lifespan)

def get_ssot_context(request: Request) -> SSOTContext:
    return request.app.state.ssot_context

# Routing
## Standard Routes & Health Check
@app.get("/", response_class=HTMLResponse)
def root(): # no check for m2m_token -> public service
    # print(f"[{datetime.now()}] [INFO] Main Page accessed!") -> debugging!
    return HTMLResponse(content=get_landing_page())

@app.get("/health")
async def health_check(): # no check for m2m_token -> public service
    print(f"[{datetime.now()}] [INFO] Health Check accesssed!") # fine for a health check to leave in place!
    return {"status": "ok", "service": "saftch-proxy"}

## AAS-Routing
@app.post("/register")
async def register_board(
    board_id: str,
    asset_type: str,
    ssot_context = Depends(get_ssot_context),
    token: str = Depends(m2m_check)
):
    print(f"[{datetime.now()}] [STAR-API] Register Board Request! Values: board_id:{board_id}; asset_type:{asset_type}")
    service = RegisterDeviceService()
    return await service.register_board(board_id, asset_type, ssot_context)

@app.post("/register_fpga_design")
async def register_fpga_design(
    design_name: str = Form(...),
    bitstream: UploadFile = File(...),
    hardwarehandoff: UploadFile = File(...),
    hiltest: UploadFile = File(...),
    additional_payload: Optional[UploadFile] = File(None),
    ssot_context = Depends(get_ssot_context),
    token: str = Depends(m2m_check)
):
    print(f"[{datetime.now()}] [STAR-API] Attempt to register new FPGA-Design: {design_name}")
    service = RegisterFpgaDesignService()
    files = {
        "bitstream": bitstream,
        "hwh": hardwarehandoff,
        "hiltest": hiltest
    }
    if additional_payload:
        files["payload"] = additional_payload

    return await service.register_design(
        design_name=design_name,
        files=files,
        ssot_context=ssot_context
    )

########## INTERNAL ROUTES FOR SELF ACCESS WITH FASTAPI
@app.get("/saftch/aas/download_fpga_design/{design_name}/{filename}")
async def download_fpga_file(
    design_name: str,
    filename: str,
    # token: str = Depends(m2m_check)
    ):
    print(f"[{datetime.now()}] [STAR-API] DOWNLOAD FPGA-Design: {design_name}! Download file: {filename}")
    file_path = Path("fpga_designs") / design_name / filename
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail=f"File {filename} not found for design {design_name}.")
    return FileResponse(path=file_path, filename=filename)

######### JOB ROUTEN
@app.get("/jobs/next")
async def get_next_job(
    ssot_context = Depends(get_ssot_context),
    token: str = Depends(m2m_check)
    ):
    print(f"[{datetime.now()}] [STAR-API] Consumer asking for new job!")
    all_shells = await ssot_context.basyxclient.get_all_shells()
    # print(all_shells) -> debugging
    for shell in all_shells:
        asset_type = shell.get("assetInformation", {}).get("assetType", "")
        if asset_type != "FPGA Design SAFTCH":
            continue
        aas_id = shell.get("id")
        target_sm_id = f"{aas_id}/sm/TestStatus"
        sm_data = await ssot_context.basyxclient.get_submodel(target_sm_id)
        # print(sm_data) -> debugging
        current_status = None
        for sme in sm_data.get("submodelElements", []):
            # print(sme) -> debugging
            # print(sme.get("idShort")) -> debugging
            if sme.get("idShort") == "Status":
                current_status = sme.get("value")
                break
        if current_status == "n/a":
            print(f"[{datetime.now()}] [STAR-API] Job available! with id: {aas_id}")
            aas_id_base64 = urlsafe_b64encode(aas_id.encode('utf-8')).decode('utf-8') # encode to safe_base64 for safe M2M-Communitcation!
            return {"job_id": aas_id_base64, "message": "Pending job found"}
    print(f"[{datetime.now()}] [STAR-API] No Job available!!")
    return {"message": "No pending jobs available", "job_id": None}

@app.get("/jobs/{job_id}/artifacts")
async def get_job_artifacts(
    job_id: str, 
    token: str = Depends(m2m_check),
    ssot_context = Depends(get_ssot_context)
):
    job_id = urlsafe_b64decode(job_id.encode('utf-8')).decode('utf-8') # immediatly overwrite to not let the base64 bleed into the proxy!
    print(f"[{datetime.now()}] [STAR-API] Daemon requested artifacts for {job_id}")
    target_sm_id = f"{job_id}/sm/FpgaDesign"
    sm_data = await ssot_context.basyxclient.get_submodel(target_sm_id)
    
    elements = {}
    for sme in sm_data.get("submodelElements", []):
        id_short = sme.get("idShort")
        value = sme.get("value")
        elements[id_short] = value
    
    async with httpx.AsyncClient() as client:
        with zipfile.ZipFile("/tmp/package.zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
            if elements.get("FileBitstream"):
                resp = await client.get(elements.get("FileBitstream"))  # type: ignore -> can not be None or Submodel is corrupt!
                resp.raise_for_status()
                zipf.writestr("design.bit", resp.content)
            if elements.get("FileHardwareHandoff"):
                print(elements.get("FileHardwareHandoff"))
                resp = await client.get(elements.get("FileHardwareHandoff")) # type: ignore -> can not be None or Submodel is corrupt!
                resp.raise_for_status()
                zipf.writestr("design.hwh", resp.content)
            if elements.get("HilTestPythonScript"):
                resp = await client.get(elements.get("HilTestPythonScript")) # type: ignore -> can not be None or Submodel is corrupt!
                resp.raise_for_status()
                zipf.writestr("hil_test.py", resp.content)
            if elements.get("AdditionalPayloadZip"):
                if elements.get("AdditionalPayloadZip") == "n/a":
                    pass
                else:
                    resp = await client.get(elements.get("AdditionalPayloadZip")) # type: ignore -> can not be None or Submodel is corrupt!
                    resp.raise_for_status()
                    payload_zip = zipfile.ZipFile(io.BytesIO(resp.content))
                    for file_info in payload_zip.infolist():
                        extracted_content = payload_zip.read(file_info.filename)
                        zipf.writestr(f"additional_payloads/{file_info.filename}", extracted_content)

    print(f"[{datetime.now()}] [STAR-API] Updating Testsstatus ssubmodell too Running {job_id}")
    target_sm_id = f"{job_id}/sm/TestStatus"
    await ssot_context.basyxclient.update_submodel_property_value_type_string(
        submodel_id=target_sm_id, 
        id_short="Status", 
        new_value="running"
    )

    return FileResponse(
        path="/tmp/package.zip",
        media_type="application/zip",
        filename="package.zip",
        background=BackgroundTask(os.remove, "/tmp/package.zip") # comment out for inspecting the file produced -> debugging
    )

@app.post("/jobs/{job_id}/result")
async def upload_job_result(
    job_id: str,
    result_file: UploadFile = File(...),
    token: str = Depends(m2m_check),
    ssot_context = Depends(get_ssot_context)
):
    job_id = urlsafe_b64decode(job_id.encode('utf-8')).decode('utf-8') # immediatly overwrite to not let the base64 bleed into the proxy!
    print(f"[{datetime.now()}] [STAR-API] Daemon uploaded result for {job_id}")
    design_name = job_id.split("/")[-1]
    save_dir = Path("fpga_designs") / design_name
    save_dir.mkdir(parents=True, exist_ok=True)
    file_path = save_dir / result_file.filename # type: ignore -> Path can never be None. HilDaemon to deterministic!
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(result_file.file, buffer)
    base_url = ssot_context.ssot_environment["BASYX_AAS_ENVIRONMENT"] 
    download_url = f"{base_url}/download_fpga_design/{design_name}/{result_file.filename}"

    print(f"[{datetime.now()}] [STAR-API] Updating FPGA Deisgn ssubmodell {job_id}")
    target_sm_id = f"{job_id}/sm/FpgaDesign"
    await ssot_context.basyxclient.update_submodel_property_value_type_string(
        submodel_id=target_sm_id, 
        id_short="ResultZip", 
        new_value=download_url
    )

    print(f"[{datetime.now()}] [STAR-API] Updating Testsstatus ssubmodell to test clonluced {job_id}")
    target_sm_id = f"{job_id}/sm/TestStatus"
    await ssot_context.basyxclient.update_submodel_property_value_type_string(
        submodel_id=target_sm_id, 
        id_short="Status", 
        new_value="Test concluded"
    )

    return {"message": "Test result uploaded and AAS updated successfully!!!", "download_url": download_url}

# Main
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)