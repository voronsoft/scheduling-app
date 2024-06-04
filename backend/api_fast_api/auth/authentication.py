import bcrypt
from typing import Annotated
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from api_fast_api.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from api_fast_api.models.models_sql import sqlalchemy_obj_to_dict, search_user_database
from api_fast_api.models.models_pydantic import UserInDBPydantic, TokenDataPydantic, UserPydantic

# Схема аутентификации OAuth2.
# Указываем страницу для авторизации/аутентификации
# Создаем экземпляр OAuth2PasswordBearer для аутентификации с использованием JWT токена
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api_admin/authorization")


# ======================== Функция для получения пользователя из базы данных по имени пользователя.
def get_user(username: str):
    """Функция для получения пользователя из базы данных по имени пользователя."""
    # Ищем пользователя в БД
    user = search_user_database(username=username)

    if user:
        # Преобразуем объект user в словарь и передаем его в конструктор UserInDBPydantic
        user_dict = sqlalchemy_obj_to_dict(user)
        return UserInDBPydantic(**user_dict)


# ======================== Функция аутентификация пользователя.
def authenticate_user(username: str, password: str):
    """
    Функция для аутентификации пользователя.
    :param username: str
    :param password: str
    :return:
    """
    user = get_user(username)  # Ищем пользователя в БД
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# ======================== Функция для создания JWT-токена.
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Функция для создания JWT-токена доступа."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# ======================== Функция для получения текущего пользователя на основе JWT-токена.
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """Функция для получения текущего пользователя на основе JWT-токена."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenDataPydantic(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)  # Ищем пользователя в БД
    if user is None:
        raise credentials_exception
    return user


# ======================== Функция для получения текущего активного пользователя.
async def get_current_active_user(current_user: Annotated[UserPydantic, Depends(get_current_user)], ):
    """Функция для получения текущего активного пользователя."""
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# ======================== Функция для проверки валидности токена
def validate_token(token: str) -> bool:
    try:
        # Декодируем токен и проверяем его подпись
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # В данном примере мы просто проверяем, что в токене есть поле 'sub'
        # Это может быть более сложная проверка в реальном приложении
        if 'sub' in payload:
            return True
    except JWTError:
        return False
    return False


# ======================== Функция для проверки пароля.
def verify_password(plain_password, hashed_password) -> bool:
    """
    Функция для проверки пароля.

    - plain_password - это незахэшированный (сырой) пароль
    - hashed_password - это хэшированный пароль из БД

    Вернет:

    - True пароли совпадают
    - False пароли не совпадают
    """
    # Сравниваем хэшированный пароль из базы данных с хэшем введённым пользователем
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


# ======================== Функция для хеширования пароля (шифрование пароля)
def get_password_hash(password: str) -> str:
    """
    Функция для хеширования пароля (шифрование пароля)

    - Принимает str
    - Возвращает str хешированный пароль (hashed password)
    """
    # Генерируем соль для усиления хэша
    salt = bcrypt.gensalt()
    # Хэшируем пароль с использованием соли
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    # Возвращаем хэшированный пароль как строку
    return hashed_password.decode('utf-8')
