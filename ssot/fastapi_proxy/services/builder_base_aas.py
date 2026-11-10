# Standard Imports
import json
# Third Party Imports
from basyx.aas import model

from basyx.aas.adapter import json as aas_json
# Local Imports

def create_base_aas(aas_id: str, id_short: str, asset_type: str) -> model.AssetAdministrationShell:
    asset_info = model.AssetInformation(
        asset_kind=model.AssetKind.INSTANCE,
        global_asset_id=f"{aas_id}_Asset",
        asset_type=asset_type
    )
    aas_object = model.AssetAdministrationShell(
        id_=aas_id,
        id_short=id_short,
        asset_information=asset_info
    )
    return json.loads(json.dumps(aas_object, cls=aas_json.AASToJsonEncoder))

def add_submodel_reference(aas_obj: model.AssetAdministrationShell, submodel_obj: model.Submodel) -> None:
    reference = model.ModelReference.from_referable(submodel_obj)
    aas_obj.submodel.add(reference)