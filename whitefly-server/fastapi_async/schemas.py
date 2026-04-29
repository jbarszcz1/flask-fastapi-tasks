from pydantic import BaseModel, field_validator


class UserCreate(BaseModel):
    name: str
    surname: str

    @field_validator('name', 'surname')
    @classmethod
    def no_digits(cls, v: str):
        if any(char.isdigit() for char in v):
            raise ValueError('Numbers are not allowed in names')
        return v
