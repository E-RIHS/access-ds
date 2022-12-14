from typing import List
from datetime import datetime, timezone

from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
import pymongo.errors


def translate_from_mongo(obj: dict):
    """
    Changes _id into id as string representation and _schema into $schema,
    and puts those fields on top
    """
    if obj is not None:
        new_obj = {"id": str(obj.pop("_id"))}
        if "_schema" in obj:
            new_obj["$schema"] = obj.pop("_schema")
        new_obj.update(obj)
        return new_obj
    else:
        return None


def translate_to_mongo(obj: dict):
    """
    Changes $schema into _schema
    """
    if obj is not None:
        if "$schema" in obj:
            new_obj = {"_schema": obj.pop("$schema")}
            new_obj.update(obj)
            return new_obj
        return obj
    else:
        return None


class NoResultsError(Exception):
    """
    Exception raised when a CRUD retrieve action does not yield results
    """
    pass


class NotCreatedError(Exception):
    """
    Exception raised when a CRUD create action does not succeed
    """
    pass


class NotUpdatedError(Exception):
    """
    Exception raised when a CRUD update action does not succeed
    """
    pass


class NotDeletedError(Exception):
    """
    Exception raised when a CRUD delete action does not succeed
    """
    pass


class DuplicateKeyError(Exception):
    """
    Exception raised when a CRUD action would result in a duplicate key
    """
    pass


class DependentObjectsError(Exception):
    """
    Exception raised when a CRUD delete action cannot be performed due 
    to existing dependent objects
    """
    pass


class CRUDBase():
    def __init__(self):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        """

    async def get(
            self, 
            collection: AsyncIOMotorCollection, 
            *,
            id: str) -> dict:
        result = await collection.find_one({"_id": ObjectId(id)})
        if result is None: raise NoResultsError
        return translate_from_mongo(result)


    async def search(
            self, 
            collection: AsyncIOMotorCollection,
            find: dict = {},
            sort_by: List[str] = [],
            sort_desc: List[bool] = [],
            skip: int = 0, 
            limit: int = 10) -> dict:
        
        if limit < 0: limit = 0
        query_parameters = {
            "skip": skip,
            "limit": limit,
            "total": await collection.count_documents(find)
        }

        if len(find) > 0: 
            query_parameters["find"] = find

        sort = []
        if len(sort_by) > 0:
            for i in range(len(sort_by)):
                if len(sort_desc) == len(sort_by):
                    sort.append((sort_by[i], -1 if sort_desc[i] == True else 1))
                else:
                    sort.append((sort_by[i], 1))
            query_parameters["sort_by"] = sort_by
            if len(sort_desc) > 0 and len(sort_desc) == len(sort_by) :
                query_parameters["sort_desc"] = sort_desc
        else:
            sort = [("$natural", pymongo.ASCENDING)]

        data = await collection.find(find).sort(sort).skip(skip).limit(limit).to_list(None)

        for i in range(len(data)):
            data[i] = translate_from_mongo(data[i])

        return {"query_parameters": query_parameters, "data": data}


    async def get_all(
            self, 
            collection: AsyncIOMotorCollection, 
            sort_by: List[str] = [],
            sort_desc: List[bool] = [],
            skip: int = 0, 
            limit: int = 10) -> dict:
        
        return await self.search(
            collection=collection, 
            sort_by=sort_by,
            sort_desc=sort_desc,
            skip=skip, 
            limit=limit)


    async def create(
            self, 
            collection: AsyncIOMotorCollection, 
            *, 
            data: dict) -> dict:
        # first encode for json, than include a datetime (to be converted to mongo date object)
        #data = data.dict()
        data = translate_to_mongo(jsonable_encoder(data))
        data["created_timestamp"] = datetime.now(timezone.utc)
        
        try: 
            insert = await collection.insert_one(data)
        except pymongo.errors.DuplicateKeyError:
            raise DuplicateKeyError

        result = await collection.find_one({"_id": insert.inserted_id})
        if result is None: raise NotCreatedError
        
        return translate_from_mongo(result)


    async def replace(
            self,
            collection: AsyncIOMotorCollection,
            id: str,
            *,
            data: dict,
            original_data: dict = None) -> dict:
        if original_data is None:
            original_data = await collection.find_one({"_id": ObjectId(id)})
            if original_data is None: raise NoResultsError

        # first encode for json, than include a datetime (to be converted to mongo date object)
        #data = data.dict()
        data = translate_to_mongo(jsonable_encoder(data))
        if "created_timestamp" in original_data:
            data["created_timestamp"] = original_data["created_timestamp"]
        data["modified_timestamp"] = datetime.now(timezone.utc)
        
        try:
            update = await collection.replace_one({"_id": ObjectId(id)}, data)
        except pymongo.errors.DuplicateKeyError:
            raise DuplicateKeyError
        
        if update.modified_count != 1: raise NotUpdatedError
        result = await collection.find_one({"_id": ObjectId(id)})
        if result is None: raise NoResultsError
        
        return translate_from_mongo(result)


    async def update(
            self,
            collection: AsyncIOMotorCollection,
            id: str,
            *,
            data: dict) -> dict:
        result = await collection.find_one({"_id": ObjectId(id)})
        if result is None: raise NoResultsError

        # first encode for json, than include a datetime (to be converted to mongo date object)
        #data = data.dict()
        data = translate_to_mongo(jsonable_encoder(data))
        data["modified_timestamp"] = datetime.now(timezone.utc)
        
        try:
            update = await collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        except pymongo.errors.DuplicateKeyError:
            raise DuplicateKeyError
        
        if update.modified_count != 1: raise NotUpdatedError
        result = await collection.find_one({"_id": ObjectId(id)})
        if result is None: raise NoResultsError
        
        return translate_from_mongo(result)
    

    async def remove(
            self,
            collection: AsyncIOMotorCollection,
            *,
            id: str)-> dict:
        result = await collection.find_one({"_id": ObjectId(id)})
        if result is None: raise NoResultsError
        
        delete = await collection.delete_one({"_id": ObjectId(id)})
        if delete.deleted_count != 1: raise NotDeletedError
        
        return translate_from_mongo(result)