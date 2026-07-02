from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime


class EmailNormalizedModel(BaseModel):
    email: str

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.lower()


class UserCreate(EmailNormalizedModel):
    password: str


class UserLogin(EmailNormalizedModel):
    password: str


class GoogleAuth(BaseModel):
    credential: str


class UserOut(BaseModel):
    email: EmailStr
    username: str
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ResultCreate(BaseModel):
    benchmark: str
    score: int
