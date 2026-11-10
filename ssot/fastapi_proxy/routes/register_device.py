import json
import httpx
from pathlib import Path
from typing import Dict, Any
from fastapi import HTTPException

import basyx.aas.model as model
import basyx.aas.adapter.aasx as aasx_adapter
import basyx.aas.adapter.json as aas_json_adapter

class RegisterDeviceService:
    def _extract_and_instantiate(self, aasx_path: Path, submodel_id: str) -> model.Submodel:
        object_store: model.DictObjectStore[model.Identifiable] = model.DictObjectStore()
        file_store = aasx_adapter.DictSupplementaryFileContainer()
        
        with aasx_adapter.AASXReader(str(aasx_path)) as reader:
            reader.read_into(object_store=object_store, file_store=file_store)
            
        submodel = object_store.get(model.Identifier(submodel_id))
        if not submodel:
            raise ValueError(f"Submodel {submodel_id} not found in {aasx_path}")
        return submodel # type: ignore -> submodel is not an identifiable...

    def _serialize(self, aas_object: model.Identifiable) -> Dict[str, Any]:
        return json.loads(json.dumps(aas_object, cls=aas_json_adapter.AASToJsonEncoder))

    async def register_board(self, board_id: str, asset_type: str, ssot_context: Any) -> dict:
        global_aas_id = f"{ssot_context.ssot_environment['AAS_IDENTIFIER_PREFIX']}/boards/{board_id}"

        asset_information = model.AssetInformation(
            asset_kind=model.AssetKind.INSTANCE,
            global_asset_id=global_aas_id + "/asset",
            asset_type="Zedboard saftch v 0.1.0"
        )
        aas_obj = model.AssetAdministrationShell(
            id_=model.Identifier(global_aas_id),
            asset_information=asset_information,
            id_short=f"AAS_{board_id}"
        )

        nameplate_sm = self._extract_and_instantiate(
            ssot_context.aas_templates.get_aasx_nameplate_prebaked_path(),
            ssot_context.aas_templates.get_id_sm_nameplate()
        )
        boardstatus_sm = self._extract_and_instantiate(
            ssot_context.aas_templates.get_aasx_boardstatus_path(),
            ssot_context.aas_templates.get_id_sm_boardstatus()
        )

        aas_obj.submodel.add(model.ModelReference.from_referable(nameplate_sm))
        aas_obj.submodel.add(model.ModelReference.from_referable(boardstatus_sm))

        aas_payload = self._serialize(aas_obj)
        nameplate_payload = self._serialize(nameplate_sm)
        boardstatus_payload = self._serialize(boardstatus_sm)

        try:
            await ssot_context.basyxclient.verify_payload(aas_payload)
            await ssot_context.basyxclient.verify_payload(nameplate_payload)
            await ssot_context.basyxclient.verify_payload(boardstatus_payload)
            
            await ssot_context.basyxclient.post_aas(aas_payload)
            await ssot_context.basyxclient.post_submodel(nameplate_payload)
            await ssot_context.basyxclient.post_submodel(boardstatus_payload)
            
            return {
                "status": "success", 
                "message": f"AAS {board_id} and 2 Submodels (Nameplate, BoardStatus) added successfully.", 
                "aas_id": global_aas_id
            }
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"BaSyx Error: {e.response.text}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))