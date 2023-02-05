from pydantic import BaseModel, Field


class _Template(BaseModel):
    id: str = Field(...)
    name: str = Field(...,
        description="Short descriptive name",
        min_length=1,
        max_length=20)
    data: dict = Field(..., description="JSON schema overlay")


class Schema(_Template):
    pass


class SchemaUi(_Template):
    pass


class SchemaI18n(_Template):
    pass


class SchemaDefaults(_Template):
    pass