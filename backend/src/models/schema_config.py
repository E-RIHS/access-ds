from typing import Optional, List

from pydantic import BaseModel, Field

from core.enums import Resource
from models.common import (
    IdBaseModel, 
    NameBaseModel, 
    QueryParameters)


class _SchemaConfig(BaseModel):
    resource: Resource = Field(...)
    category: Optional[str] = Field(None, 
        description="Category identifier",
        min_length=1,
        max_length=20)
    json_schema: str = Field(...)
    ui_schema: Optional[str] = Field(None)
    i18n_schema: Optional[str] = Field(None)
    default_dataset: Optional[str] = Field(None)
    draft: bool = Field(False)
    depreciated: bool = Field(False)


class _Resolved(BaseModel):
    json_schema_resolved: dict = Field(...)
    ui_schema_resolved: Optional[dict] = Field(None)
    i18n_schema_resolved: Optional[dict] = Field(None)
    default_dataset_resolved: Optional[dict] = Field(None)

class SchemaConfig(_Resolved, _SchemaConfig, NameBaseModel, IdBaseModel):
    pass


class SchemaConfigShort(_SchemaConfig, NameBaseModel, IdBaseModel):
    pass


class SchemaConfigUpdate(_SchemaConfig, NameBaseModel):
    pass


class SchemaConfigList(BaseModel):
    query_parameters: QueryParameters = Field(...)
    data: List[SchemaConfigShort] = Field([])