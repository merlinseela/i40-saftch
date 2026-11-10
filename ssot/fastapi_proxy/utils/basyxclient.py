# Standard Library Imports
from base64 import urlsafe_b64decode, urlsafe_b64encode
# Third Party Imports
from httpx import AsyncClient
# Local Imports


class BasyxAPIClient:
    def __init__(self, base_url: str):
        self.client = AsyncClient(base_url=base_url)

    async def close(self) -> None:
        await self.client.aclose()

    async def verify_payload(self, payload: dict) -> bool:
        response = await self.client.post("/verify", json=payload)
        response.raise_for_status()
        return True

    async def get_all_shells(self) -> dict:
        response = await self.client.get("/shells")
        response.raise_for_status()
        payload = response.json()
        return payload.get("result", [])

    async def get_submodel(self, submodel_id: str) -> dict:
        encoded_id = urlsafe_b64encode(submodel_id.encode('utf-8')).decode('utf-8')
        response = await self.client.get(f"/submodels/{encoded_id}")
        response.raise_for_status()
        return response.json()

    async def post_aas(self, payload: dict) -> bool:
        response = await self.client.post("/shells", json=payload)
        response.raise_for_status()
        return True

    async def post_submodel(self, payload: dict) -> bool:
        response = await self.client.post("/submodels", json=payload)
        response.raise_for_status()
        return True

    async def update_submodel_property_value_type_string(self, submodel_id: str, id_short: str, new_value: str) -> bool:
        encoded_sm_id = urlsafe_b64encode(submodel_id.encode('utf-8')).decode('utf-8')
        payload = {
            "idShort": id_short,
            "modelType": "Property",
            "valueType": "xs:string", 
            "value": new_value
        }
        response = await self.client.put(
            f"/submodels/{encoded_sm_id}/submodel-elements/{id_short}",
            json=payload
        )
        response.raise_for_status()
        return True