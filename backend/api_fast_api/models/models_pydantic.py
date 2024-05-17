from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, conint, Field, SecretStr


class ReceivingDataFromCalendarPydantic(BaseModel):
    """Модель данных при заявке на урок с календаря"""
    name: str = Field(..., description="First name of the applicant", example="Name")
    surname: str = Field(..., description="Last name of the applicant", example="Last")
    phone: str = Field(..., description="Only numbers", example="123456789")
    email: EmailStr = Field(..., description="Email address of the applicant")
    selectedDate: str = Field(..., description="Selected date in the format YYYY-MM-DD", example="2024-05-20")
    time: str = Field(..., description="Time of the lesson", example=14)
    # confirmed: bool = Field(..., description="lesson status", example=False)


class RegistrationUserPydantic(BaseModel):
    """Модель данных при регистрации пользователя"""
    username: str = Field(..., description="Name user", example="jon")
    email: EmailStr = Field(..., description="Email address user", example="jon@jon.jon")
    password: SecretStr = Field(..., description="Password user", example="jon")


class AuthorizationUserPydantic(BaseModel):
    """Модель данных при авторизации пользователя"""
    username: str = Field(..., description="Name user", example="jon")
    email: str | None = Field(None, description="Email address user", example="jon@jon.jon")
    password: SecretStr = Field(..., description="Password user", example="jon")
    uuid: Optional[UUID] = None


# --------------------------------------------
# Модель токена для ответа на запрос аутентификации.
class TokenPydantic(BaseModel):
    """Модель токена"""
    access_token: str
    token_type: str


# Модель данных токена.
class TokenDataPydantic(BaseModel):
    username: str | None = None


# Модель пользователя.
class UserPydantic(BaseModel):
    """Модель пользователя """
    username: str
    last_name: str | None = None
    email: str | None = None
    uuid: UUID | None = None
    disabled: bool | None = None


# Модель пользователя в базе данных.
class UserInDBPydantic(UserPydantic):
    hashed_password: str
