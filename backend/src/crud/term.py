from typing import Optional, List

from motor.motor_asyncio import AsyncIOMotorCollection

from crud.base import CRUDBase, NoResultsError


class CRUDTerm(CRUDBase):
    async def get_children(
            self, 
            collection: AsyncIOMotorCollection, 
            *,
            parent_id: str = "_root") -> dict:
        result = await self.search(
            collection=collection,
            find={"instance_of": parent_id}, 
            limit=0)
        if len(result['data']) == 0:
            raise NoResultsError
        return result['data']
    

    async def get_children_localised(
            self, 
            collection: AsyncIOMotorCollection, 
            *,
            parent_id: str = "_root",
            lang: str = "en") -> dict:
        result = await self.get_children(
            collection=collection,
            parent_id=parent_id)
        for term in result:
            localised_label: str = ""
            localised_description: Optional[str] = None
            if lang in term["label"]:
                localised_label = term["label"][lang]
            elif "en" in term["label"]:
                localised_label = term["label"]["en"]
            else:
                localised_label = term["name"]
            if lang in term["description"]:
                localised_description = term["description"][lang]
            elif "en" in term["description"]:
                localised_description = term["description"]["en"]
            term['label'] = localised_label
            term['description'] = localised_description
        # sort on label
        return sorted(result, key=lambda d: d['label']) 

    
term = CRUDTerm()

