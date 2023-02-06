
from typing import List

from pydantic import BaseModel, Field

from models.common import (
    IdBaseModel, 
    NameBaseModel, 
    DataBaseModel, 
    LoggingBaseModel, 
    QueryParameters)


class DefaultDataset(LoggingBaseModel, DataBaseModel, NameBaseModel, IdBaseModel):
    pass


class DefaultDatasetShort(NameBaseModel, IdBaseModel):
    pass


class DefaultDatasetUpdate(DataBaseModel, NameBaseModel):
    pass


class DefaultDatasetList(BaseModel):
    query_parameters: QueryParameters = Field(...)
    data: List[DefaultDatasetShort] = Field([])