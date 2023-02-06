
from typing import Optional

from pydantic import BaseModel, Field

from core.enums import Resource


class SchemaConfig(BaseModel):
    id: str = Field(...)
    name: str = Field(...,
        description="Short descriptive name",
        min_length=1,
        max_length=20)
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