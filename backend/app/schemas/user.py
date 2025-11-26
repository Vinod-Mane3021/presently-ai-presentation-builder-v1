from typing import Any
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=1, max_length=255)
    providers: list[str] | None = None
    picture_url: str | None = None
    user_metadata: dict[str, Any] | None = None
    last_signin_at: datetime | None = None
    created_by: UUID | None = None
    updated_by: UUID | None = None

class UserOut(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2 "ORM mode"


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=255)


class UserSignin(BaseModel):
    email: EmailStr | None = None
    password: str = Field(min_length=8, max_length=255)


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = Field(default=None, min_length=1, max_length=255)
    providers: list[str] | None = None
    picture_url: str | None = None
    user_metadata: dict[str, Any] | None = None
    last_signin_at: datetime | None = None
    updated_by: UUID | None = None
