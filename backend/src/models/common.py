from typing import Optional, Literal, List, Set
from enum import Enum
from datetime import datetime, date

from pydantic import BaseModel, Field


class IdBaseModel(BaseModel):
    id: str = Field(...)


class NameBaseModel(BaseModel):
    name: str = Field(...,
        description="Short descriptive name",
        min_length=1,
        max_length=100)


class DataBaseModel(BaseModel):
    data: dict = Field(...)


class LoggingBaseModel(BaseModel):
    created_timestamp: Optional[datetime] = Field(None)
    created_by_user: Optional[str] = Field(None)
    modified_timestamp: Optional[datetime] = Field(None)
    modified_by_user: Optional[str] = Field(None)


class QueryParameters(BaseModel):
    find: Optional[dict] = Field({})
    sort_by: Optional[List[str]] = Field([])
    sort_desc: Optional[List[bool]] = Field([])
    skip: Optional[int] = Field(0)
    limit: Optional[int] = Field(10)
    total: int = Field(...)