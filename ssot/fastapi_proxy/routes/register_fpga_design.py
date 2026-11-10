import json
import httpx
import shutil
from pathlib import Path
from typing import Dict, Any
from fastapi import HTTPException

import basyx.aas.model as model
import basyx.aas.adapter.aasx as aasx_adapter
import basyx.aas.adapter.json as aas_json_adapter

class RegisterFpgaDesignService:
    def _extract_and_instantiate(self, aasx_path: Path, submodel_id: str) -> model.Submodel:
        object_store: model.DictObjectStore[model.Identifiable] = model.DictObjectStore()
        file_store = aasx_adapter.DictSupplementaryFileContainer()
        
        with aasx_adapter.AASXReader(str(aasx_path)) as reader:
            reader.read_into(object_store=object_store, file_store=file_store)
            
        submodel = object_store.get(model.Identifier(submodel_id))
        if not submodel:
            raise ValueError(f"Submodel {submodel_id} not found in {aasx_path}")
            
        submodel.kind = model.ModellingKind.INSTANCE # type:ignore -> KIND IS MODELLINGKIND!
        return submodel # type:ignore -> submodel is not an Identifiable...

    def _serialize(self, aas_object: model.Identifiable) -> Dict[str, Any]:
        return json.loads(json.dumps(aas_object, cls=aas_json_adapter.AASToJsonEncoder))

    async def register_design(self, design_name: str, files: dict, ssot_context: Any) -> dict:
        global_aas_id = f"{ssot_context.ssot_environment['AAS_IDENTIFIER_PREFIX']}/fpga_design/{design_name}"
        # print(global_aas_id) -> debugging
        asset_information = model.AssetInformation(
            asset_kind=model.AssetKind.INSTANCE,
            global_asset_id=global_aas_id + "/asset",
            asset_type="FPGA Design SAFTCH"
        )
        aas_obj = model.AssetAdministrationShell(
            id_=model.Identifier(global_aas_id),
            asset_information=asset_information,
            id_short=f"AAS_{design_name}"
        )

        # fpgadesign SM
        fpgadesign_sm = self._extract_and_instantiate(
            ssot_context.aas_templates.get_aasx_fpgadesign_path(),
            ssot_context.aas_templates.get_id_sm_fpgadessign()
        )
        fpgadesign_sm.id = f"{global_aas_id}/sm/FpgaDesign"
        base_url = ssot_context.ssot_environment['AAS_IDENTIFIER_PREFIX']
        for sme in fpgadesign_sm.submodel_element:
            if sme.id_short == "FileBitstream" and files.get("bitstream"):
                sme.value = f"{base_url}/download_fpga_design/{design_name}/{files['bitstream'].filename}" # type:ignore Yes a SubModelElement has a value if it is a Property!
            if sme.id_short == "FileHardwareHandoff" and files.get("hwh"):
                sme.value = f"{base_url}/download_fpga_design/{design_name}/{files['hwh'].filename}" # type:ignore Yes a SubModelElement has a value if it is a Property!
            if sme.id_short == "HilTestPythonScript" and files.get("hiltest"):
                sme.value = f"{base_url}/download_fpga_design/{design_name}/{files['hiltest'].filename}" # type:ignore Yes a SubModelElement has a value if it is a Property!
            if sme.id_short == "AdditionalPayloadZip" and files.get("payload"):
                sme.value = f"{base_url}/download_fpga_design/{design_name}/{files['payload'].filename}" # type:ignore Yes a SubModelElement has a value if it is a Property!
        aas_obj.submodel.add(model.ModelReference.from_referable(fpgadesign_sm))

        # TestStatus SM
        teststatus_sm = self._extract_and_instantiate(
            ssot_context.aas_templates.get_aasx_teststatus_path(),
            ssot_context.aas_templates.get_id_sm_teststatus()
        )
        teststatus_sm.id = f"{global_aas_id}/sm/TestStatus"
        aas_obj.submodel.add(model.ModelReference.from_referable(teststatus_sm))

        aas_payload = self._serialize(aas_obj)
        fpgadesign_payload = self._serialize(fpgadesign_sm)
        teststatus_payload = self._serialize(teststatus_sm)
        try:
            await ssot_context.basyxclient.verify_payload(aas_payload)
            await ssot_context.basyxclient.verify_payload(fpgadesign_payload)
            await ssot_context.basyxclient.verify_payload(teststatus_payload)

            await ssot_context.basyxclient.post_aas(aas_payload)
            await ssot_context.basyxclient.post_submodel(fpgadesign_payload)
            await ssot_context.basyxclient.post_submodel(teststatus_payload)
            
            save_dir = Path("fpga_designs") / design_name
            save_dir.mkdir(parents=True, exist_ok=True)
        
            saved_files = []
            for key, upload_file in files.items():
                if not upload_file: # optional-upload will crash if not existend
                    continue
                file_path = save_dir / upload_file.filename
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(upload_file.file, buffer)
                saved_files.append(str(file_path))

            return {
                "status": "success", 
                "message": f"FPGA Design AAS '{design_name}' and Submodels verified.", 
                "aas_id": global_aas_id,
                "received_files": list(files.keys())
            }
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"BaSyx Error: {e.response.text}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))