from typing import Optional, List

from pydantic import BaseModel, Field

from models.common import IdBaseModel, QueryParameters


class TermUpdate(BaseModel):
    name: str = Field(..., min_length=1)
    instance_of: str = Field(..., min_length=1)
    label: dict = Field(...)
    description: Optional[dict] = Field(None)
    same_as: Optional[str] = Field(None)
    source: Optional[str] = Field(None)


class Term(TermUpdate, IdBaseModel):
    instance_of: Optional[str] = Field(None)


class TermShort(IdBaseModel):
    name: str = Field(..., min_length=1)
    label: dict = Field(...)


class TermLocalised(IdBaseModel):
    name: str = Field(...)
    label: str = Field(...)
    #description: Optional[str] = Field(None)


class TermChildren(BaseModel):
    data: List[TermShort] = Field(...)


class TermChildrenLocalised(BaseModel):
    data: List[TermLocalised] = Field(...)


class TermList(BaseModel):
    query_parameters: QueryParameters = Field(...)
    data: List[TermShort] = Field([])