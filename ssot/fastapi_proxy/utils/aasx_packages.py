# simple utility classs to reduce mental load in god scripts
# Standard Library Imports
# Third Party Imports
# Local Imports
import basyx.aas.adapter.aasx as aasx_adapter
import basyx.aas.adapter.json as aas_json_adapter
from typing import Any
import json
from pathlib import Path
from typing import Dict
import basyx.aas.model as model

def extract_and_instantiate(aasx_path: Path, submodel_id: str) -> model.Submodel:
        object_store: model.DictObjectStore[model.Identifiable] = model.DictObjectStore()
        file_store = aasx_adapter.DictSupplementaryFileContainer()
        
        with aasx_adapter.AASXReader(str(aasx_path)) as reader:
            reader.read_into(object_store=object_store, file_store=file_store)
            
        submodel = object_store.get(model.Identifier(submodel_id))
        if not submodel:
            raise ValueError(f"Submodel {submodel_id} not found in {aasx_path}")
            
        submodel.kind = model.ModellingKind.INSTANCE # type:ignore -> KIND IS MODELLINGKIND!
        return submodel # type:ignore -> submodel is not an Identifiable...

def serialize(aas_object: model.Identifiable) -> Dict[str, Any]:
    return json.loads(json.dumps(aas_object, cls=aas_json_adapter.AASToJsonEncoder))