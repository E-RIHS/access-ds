from typing import List

from pydantic import BaseModel, Field

from models.common import (
    IdBaseModel, 
    NameBaseModel, 
    DataBaseModel, 
    QueryParameters)


class I18nSchema(DataBaseModel, NameBaseModel, IdBaseModel):
    pass


class I18nSchemaShort(NameBaseModel, IdBaseModel):
    pass


class I18nSchemaUpdate(DataBaseModel, NameBaseModel):
    pass


class I18nSchemaList(BaseModel):
    query_parameters: QueryParameters = Field(...)
    data: List[I18nSchemaShort] = Field([])