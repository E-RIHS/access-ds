from pydantic import BaseModel, Field


class _IdNameBaseModel(BaseModel):
    id: str = Field(...)
    name: str = Field(...,
        description="Short descriptive name",
        min_length=1,
        max_length=20)


class _DataBaseModel(BaseModel):
    data: dict = Field(..., description="JSON schema overlay")


class Schema(_IdNameBaseModel, _DataBaseModel):
    pass


class SchemaShort(_IdNameBaseModel):
    pass


class SchemaUi(_IdNameBaseModel, _DataBaseModel):
    pass


class SchemaUiShort(_IdNameBaseModel):
    pass


class SchemaI18n(_IdNameBaseModel, _DataBaseModel):
    pass


class SchemaI18nShort(_IdNameBaseModel):
    pass


class SchemaDefaults(_IdNameBaseModel, _DataBaseModel):
    pass


class SchemaDefaultsShort(_IdNameBaseModel):
    pass