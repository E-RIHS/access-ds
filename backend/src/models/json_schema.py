from typing import List

from pydantic import BaseModel, Field

from models.common import (
    IdBaseModel, 
    NameBaseModel, 
    DataBaseModel, 
    LoggingBaseModel, 
    QueryParameters)


class JsonSchema(LoggingBaseModel, DataBaseModel, NameBaseModel, IdBaseModel):
    pass


class JsonSchemaShort(NameBaseModel, IdBaseModel):
    pass


class JsonSchemaUpdate(DataBaseModel, NameBaseModel):
    pass


class JsonSchemaList(BaseModel):
    query_parameters: QueryParameters = Field(...)
    data: List[JsonSchemaShort] = Field([])