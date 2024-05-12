from typing import Annotated
from datetime import timedelta

from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import APIRouter, Depends, Request, Response, status, HTTPException

from backend.api_fast_api.config import ACCESS_TOKEN_EXPIRE_MINUTES
from backend.api_fast_api.auth.authentication import create_access_token, authenticate_user, get_current_active_user, get_password_hash
from backend.api_fast_api.models.models_pydantic import RegistrationUserPydantic, TokenPydantic, UserPydantic
from backend.api_fast_api.models.models_sql import get_lessons_for_month, lesson_dates_for_the_month_db, save_user_registration

# Создаем экземпляр APIRouter с префиксом
router_admin = APIRouter(prefix="/api_admin")
tags_metadata_admin = [{"name": "ADMINpanel", "description": "Маршруты админ панели"}, ]
# Создаем экземпляр OAuth2PasswordBearer для аутентификации с использованием JWT токена
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api_admin/authorization")


# -----------------------------------------------------------------------------------------------------------------
# Маршрут регистрации пользователя
@router_admin.post("/registration", include_in_schema=False, tags=["ADMINpanel"])
async def register_user(user_data: RegistrationUserPydantic, response: Response, request: Request):
    """
    **Метод POST**

    **Маршрут регистрации**
    Параметры:
    - username: str
    - email: str
    - password: str

    Возвращаемые данные:

    ...

    Возможные статусы ответа:

    - 201: Успешный запрос. Возвращается словарь с токеном.
    - 409: Некорректный email. Такой пользователь уже существует.
    - 500: Внутренняя ошибка сервера. Возвращается описание ошибки.

    Ссылка для запроса:

    - http://example.com/api_admin/registration

    Пример ответа:

    - 201: {"token": token}
    - 409: {"message": "A user with this email already exists!"}
    - 500: {"error": description error}
    """
    # Получаем данные пользователя из объекта user_data
    username = user_data.username
    # Получаем адрес почты
    email = user_data.email
    # Используем get_secret_value() для получения значения пароля в понятном читаемом виде.
    password = user_data.password.get_secret_value()

    print("username", username)
    print("email", email)
    print("password", password)

    # Хешируем полученный пароль из запроса на регистрацию
    hashed_password = get_password_hash(password)
    # Сохраняем данные нового пользователя в базе данных
    print("hashed_password", hashed_password)
    print("-----------")
    print()

    # Передаем данные в функцию для записи нового пользователя в БД
    sts, result = save_user_registration(username, email, hashed_password)
    if sts == 201:
        response.status_code = status.HTTP_201_CREATED
        return {"message": "The user has successfully registered!"}
    elif sts == 409:
        response.status_code = status.HTTP_409_CONFLICT
        return {"message": "A user with this email already exists!"}
    elif sts == 500:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"Error": result}


# -----------------------------------------------------------------------------------------------------------------
# Маршрут для получения JWT-токена доступа.
@router_admin.post("/authorization", include_in_schema=False, tags=["ADMINpanel"])
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], request: Request) -> TokenPydantic:
    """Маршрут для получения JWT-токена доступа."""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return TokenPydantic(access_token=access_token, token_type="bearer")


# -----------------------------------------------------------------------------------------------------------------

# Маршрут получение списка дат уроков на запрашиваемый месяц.
@router_admin.get("/lesson_dates_for_the_month/{date_in}", tags=["ADMINpanel"], status_code=200)
async def get_lesson_dates_for_the_month(date_in: str, response: Response):
    """
    **Метод: GET**

    **Маршрут получение списка дат уроков на запрашиваемый месяц**
    Параметры:
    - date_in: Дата в формате YYYY-MM-DD. 2024-04-27

    Возвращаемые данные:
    - Словарь с данными о бронировании на указанную дату.
      Пример: {"2024-04-24": "true", "2024-04-30": "await"}
      true - дата одобрена, await - дата в ожидании.

    Возможные статусы ответа:
    - 200: Успешный запрос. Возвращается словарь с данными о бронировании.
    - 404: Даты занятий не найдены в бд на запрашиваемый месяц
    - 422: Некорректный формат даты. Возвращается детальное описание ошибки.
    - 500: Внутренняя ошибка сервера. Возвращается описание ошибки.

    Примеры использования:
    - http://example.com/api_admin/lesson_dates_for_the_month/2024-9-24
    - http://example.com/api_admin/lesson_dates_for_the_month/2024-09-24
    Пример ответа:
    - 200: {"2024-4-24": "true","2024-4-30": "await"}

    - 404: {"Not found"} Даты на этот месяц не найдены.

    - 422:{"detail": "Invalid date format"}

    - 500:{"detail": "Internal Server Error: Something went wrong"}
    """

    code, data = lesson_dates_for_the_month_db(date_in)

    if code == 500:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return data
    elif code == 200:
        response.status_code = status.HTTP_200_OK
        return data
    elif code == 404:
        response.status_code = status.HTTP_404_NOT_FOUND
        return data
    elif code == 422:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return data


# -----------------------------------------------------------------------------------------------------------------

# TODO Защищенный маршрут, требующий аутентификации На момент разработки отключено
# Маршрут получения занятий на запрашиваемый месяц
@router_admin.get("/get_lessons_for_a_month/{date_y_m_d}", tags=["ADMINpanel"], status_code=200)
# async def get_lessons_for_a_month(date_y_m_d: str, response: Response, current_user: Annotated[UserPydantic, Depends(get_current_active_user)]):
async def get_lessons_for_a_month(date_y_m_d: str, response: Response):
    """
    **Метод: GET**

    **Маршрут получения занятий на запрашиваемый месяц**

    Параметры:
    - date_in: Дата в формате YYYY-MM-DD. Тип строка.

    Возвращаемые данные:
    - Словарь с данными о бронировании на указанную дату месяца.\n
            {"lessons": [{
                            "id": 1,
                            "username": "Name1",
                            "last_name": "1",
                            "email": "er@er.com",
                            "phone": "123-45-67",
                            "selected_date": "2024-04-25",
                            "selected_time": "15",
                            "confirmed_state": "false"
                            },
                            ]}

    Возможные статусы ответа:
    - 200: Вернет список дат связанных с запрашиваемым месяцем.
    - 404: Не найдено записей.
    - 422: Некорректный формат даты в запросе. Возвращается детальное описание ошибки.
    - 500: Внутренняя ошибка сервера. Возвращается описание ошибки.

    Примеры использования:
    - http://example.com/api_admin/get_lessons_for_a_month/2024-2-20
    - http://example.com/api_admin/get_lessons_for_a_month/2024-04-20

    Пример ответа:

    - 200:

            {"lessons": [{
                      "id": 1,
                      "username": "Name1",
                      "last_name": "1",
                      "email": "er@er.com",
                      "phone": "123-45-67",
                      "selected_date": "2024-04-25",
                      "selected_time": "15",
                      "confirmed_state": "false"
                    },
                    {
                      "id": 6,
                      "username": "Name6",
                      "last_name": "Last",
                      "email": "user@exa1mple.com",
                      "phone": "123456789",
                      "selected_date": "2024-04-25",
                      "selected_time": "14",
                      "confirmed_state": "false"
                    }]
            }

    - 404:{"lessons": "Not found"}

    - 422: {"detail": "Invalid date format"}

    - 500: {"detail": error description}
    """
    sts, lessons = get_lessons_for_month(date_y_m_d)
    if sts == 200:
        response.status_code = status.HTTP_200_OK
        return {"lessons": lessons}

    elif sts == 404:
        response.status_code = status.HTTP_404_NOT_FOUND
        return lessons
    elif sts == 422:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return lessons
    elif sts == 500:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return lessons


# -----------------------------------------------------------------------------------------------------------------

# TODO в разработке /logout
# Маршрут выхода пользователя
@router_admin.post("/logout", include_in_schema=False, tags=["ADMINpanel"])
async def logout_user(request: Request):
    """
    **Метод: POST**

    **Маршрут выхода пользователя**
    В разработке !!!

    - Принимает:

        token: str

        flag: False or True (str)

    - Возвращает: json

        {status: status, message: message}
    """
    ...
    # print("--------------------")
    # pprint(request.__dict__)
    return "Вы попытались выйти из системы но этот метод еще не реализован !!!"
