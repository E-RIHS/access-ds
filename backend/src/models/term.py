from typing import Optional, List

from pydantic import BaseModel, Field

from models.common import IdBaseModel


class TermUpdate(BaseModel):
    name: str = Field(..., min_length=1)
    instance_of: str = Field(..., min_length=1)
    label: dict = Field(...)
    description: Optional[dict] = Field(None)
    same_as: Optional[str] = Field(None)
    source: Optional[str] = Field(None)


class Term(TermUpdate, IdBaseModel):
    pass


class TermLocalised(IdBaseModel):
    name: str = Field(...)
    label: str = Field(...)
    description: Optional[str] = Field(None)


class TermChildren(BaseModel):
    children: List[Term] = Field(...)


class TermChildrenLocalised(BaseModel):
    children: List[TermLocalised] = Field(...)
