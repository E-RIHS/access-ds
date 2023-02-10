from typing import Optional, List

from pydantic import BaseModel, Field

from core.enums import Resource
from models.common import (
    IdBaseModel, 
    NameBaseModel, 
    LoggingBaseModel, 
    QueryParameters)


class _SchemaConfigBase(BaseModel):
    resource: Resource = Field(...)
    category: str = Field(..., 
        description="Category identifier",
        min_length=1,
        max_length=20)
    json_schema: str = Field(...)
    schema_ui: Optional[str] = Field(None)
    schema_i18n: Optional[str] = Field(None)
    schema_defaults: Optional[str] = Field(None)
    active: bool = Field(False)
    depreciated: bool = Field(False)


class SchemaConfig(LoggingBaseModel, _SchemaConfigBase, NameBaseModel, IdBaseModel):
    pass


class SchemaConfigShort(_SchemaConfigBase, NameBaseModel, IdBaseModel):
    pass


class SchemaConfigUpdate(_SchemaConfigBase, NameBaseModel):
    pass


class SchemaConfigList(BaseModel):
    query_parameters: QueryParameters = Field(...)
    data: List[SchemaConfigShort] = Field([])