from typing import List

from pydantic import BaseModel, Field

from models.common import (
    IdBaseModel, 
    NameBaseModel, 
    DataBaseModel, 
    QueryParameters)


class UiSchema(DataBaseModel, NameBaseModel, IdBaseModel):
    pass


class UiSchemaShort(NameBaseModel, IdBaseModel):
    pass


class UiSchemaUpdate(DataBaseModel, NameBaseModel):
    pass


class UiSchemaList(BaseModel):
    query_parameters: QueryParameters = Field(...)
    data: List[UiSchemaShort] = Field([])