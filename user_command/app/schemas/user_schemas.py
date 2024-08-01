from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class UserModel(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class UserCreateModel(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "username": "johndoe",
                "email": "johndoe@gmail.com",
                "first_name": "John",
                "last_name": "Doe"
            }
        }
    )


class UserUpdateModel(BaseModel):
    username: Optional[str]
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "username": "johndoe",
                "email": "johnnydoe@gmail.com",
                "first_name": "Johnny",
                "last_name": "Doe"
            }
        }
    )
