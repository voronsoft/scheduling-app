import re
from uuid import UUID
from datetime import date
from typing import Optional, Any
from pydantic import BaseModel, EmailStr, Field, SecretStr, field_validator


# -------------- Модель приема данных с формы календаря для записи занятия в бд
class ReceivingDataFromCalendarPydantic(BaseModel):
    """Модель данных при заявке на урок с календаря"""
    name: str = Field(..., description="First name of the applicant", example="Name")
    surname: str = Field(..., description="Last name of the applicant", example="Last")
    phone: str = Field(..., description="Only numbers", example="123456789")
    email: EmailStr = Field(..., description="Email address of the applicant")
    selectedDate: str = Field(..., description="Selected date in the format YYYY-MM-DD", example="2024-05-20")
    time: str = Field(..., description="Time of the lesson", example=14)
    # confirmed: bool = Field(..., description="lesson status", example=False)


# -------------- Модель данных для регистрации пользователя
class RegistrationUserPydantic(BaseModel):
    """Модель данных для регистрации пользователя"""
    username: str = Field(..., description="Name user", example="jon")
    email: EmailStr = Field(..., description="Email address user", example="jon@jon.jon")
    password: SecretStr = Field(..., description="Password user", example="jon")


# -------------- Модель данных для авторизации пользователя
class AuthorizationUserPydantic(BaseModel):
    """Модель данных для авторизации пользователя"""
    username: str = Field(..., description="Name user", example="jon")
    email: str | None = Field(None, description="Email address user", example="jon@jon.jon")
    password: SecretStr = Field(..., description="Password user", example="jon")
    uuid: Optional[UUID] = None


# -------------- Модель токена для ответа на запрос аутентификации.
class TokenPydantic(BaseModel):
    """Модель токена"""
    access_token: str
    token_type: str


# -------------- Модель данных токена.
class TokenDataPydantic(BaseModel):
    username: str | None = None


# -------------- Модель пользователя.
class UserPydantic(BaseModel):
    """Модель пользователя """
    username: str
    last_name: str | None = None
    email: str | None = None
    uuid: UUID | None = None
    disabled: bool | None = None


# -------------- Модель пользователя в базе данных.
class UserInDBPydantic(UserPydantic):
    hashed_password: str


# -------------- Модель проверки даты
class DateModelPydantic(BaseModel):
    """Проверка даты (2024-1-24)"""
    date: str


# -------------- Модель данных изменения полей записи урока
class UpdateLessonDataPydantic(BaseModel):
    """Модель данных изменения полей записи урока"""
    username: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    selected_date: Optional[str] = None
    time: Optional[str] = None
    confirmed: Optional[bool] = None
