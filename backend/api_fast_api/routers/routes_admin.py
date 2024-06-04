from typing import Annotated
from datetime import timedelta

from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import APIRouter, Depends, Request, Response, status, HTTPException

from api_fast_api.config import ACCESS_TOKEN_EXPIRE_MINUTES
from api_fast_api.auth.authentication import create_access_token, authenticate_user, get_password_hash
from api_fast_api.models.models_pydantic import RegistrationUserPydantic, TokenPydantic
from api_fast_api.models.models_sql import get_lessons_for_month, lesson_dates_for_the_month_db, save_user_registration

router_admin = APIRouter(prefix="/api_admin")  # Создаем экземпляр APIRouter с префиксом
tags_metadata_admin = [{"name": "ADMINpanel", "description": "Маршруты админ панели"}, ]


# ======================== Маршрут регистрации пользователя ========================
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
        return {"message": "A user with this email already exists! / The user limit is limited!"}
    elif sts == 500:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"Error": result}


# ======================== Маршрут для получения JWT-токена доступа. ========================
@router_admin.post("/authorization", include_in_schema=True, tags=["ADMINpanel"])
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], request: Request
                                 ) -> TokenPydantic:
    """
    **Метод POST**

    **Маршрут для получения JWT-токена доступа.**
    Параметры:
    - username: str
    - email: str
    - password: str

    Возвращаемые данные:

        {
          "access_token": "string",
          "token_type": "string"
        }


    Возможные статусы ответа:

    - 200: Успешный запрос. Возвращается словарь с токеном.
    - 401: Incorrect username or password
    - 500: Внутренняя ошибка сервера. Возвращается описание ошибки.

    Ссылка для запроса:

    - http://example.com/api_admin/authorization

    Пример ответа:

    - 200: {"access_token": "bearer", "token_type": "som_token_string"}
    - 401: {"detail": "Incorrect username or password"}
    - 500: {"error": description error}

    """
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


# ========================  ========================
@router_admin.get("/lesson_dates_for_the_month/{date_in}", tags=["ADMINpanel"], status_code=200)
async def get_lesson_dates_for_the_month(date_in: str, response: Response):
    """
    **Метод: GET**

    **Маршрут получение списка дат уроков на запрашиваемый месяц**
    Параметры:
    - date_in: Дата в формате YYYY-MM-DD. 2024-04-27

    Возвращаемые данные:
    - Словарь с данными о бронировании на указанную дату.
      Пример: {"2024-04-24": True, "2024-04-30": False}
      True - дата одобрена, False - дата в ожидании.

    Возможные статусы ответа:
    - 200: Успешный запрос. Возвращается словарь с данными о бронировании.
    - 404: Даты занятий не найдены в бд на запрашиваемый месяц
    - 422: Некорректный формат даты. Возвращается детальное описание ошибки.
    - 500: Внутренняя ошибка сервера. Возвращается описание ошибки.

    Примеры использования:
    - http://example.com/api_admin/lesson_dates_for_the_month/2024-9-24
    - http://example.com/api_admin/lesson_dates_for_the_month/2024-09-24

    Пример ответа:
    - 200: {"2024-4-24": True,"2024-4-30": False}
    - 404: {"Not found"} Даты на этот месяц не найдены.
    - 422:{"detail": "Invalid date format"}
    - 500:{"detail": "Internal Server Error: Something went wrong"}
    """

    code, data = lesson_dates_for_the_month_db(date_in)

    if code == 200:
        response.status_code = status.HTTP_200_OK
        return data
    elif code == 404:
        response.status_code = status.HTTP_404_NOT_FOUND
        return data
    elif code == 422:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return data
    elif code == 500:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return data


# ======================== Маршрут получения занятий на запрашиваемый месяц ========================
@router_admin.get("/get_lessons_for_a_month/{date_y_m_d}", tags=["ADMINpanel"], status_code=200)
async def get_lessons_for_a_month(date_y_m_d: str, response: Response):
    """
    **Метод: GET**

    **Маршрут получения занятий на запрашиваемый месяц (полные данные о заявке)**

    Параметры принимает:
    - date_in: Дата в формате YYYY-MM-DD. Тип строка. (2024-05-16)

    Возвращаемые данные:
    - Словарь с данными о бронировании на указанную дату месяца.

            {"lessons": [
                            {
                            "id": 1,
                            "email": "er@er.com",
                            "firstName": "Name1",
                            "lastName": "1",
                            "phone": "123-45-67",
                            "selectedDate": "2024-04-25",
                            "selectedTime": "15",
                            "confirmed": false
                            },
                        ]
            }

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

            {"lessons": [
                            {
                                "id": 1,
                                "email": "er@er.com",
                                "firstName": "Name1",
                                "lastName": "1",
                                "phone": "123-45-67",
                                "selectedDate": "2024-04-25",
                                "selectedTime": "15",
                                "confirmed": false
                            },
                            {
                                "id": 2,
                                "email": "2er@er.com",
                                "firstName": "Name2",
                                "lastName": "2",
                                "phone": "222-22-22",
                                "selectedDate": "2024-02-22",
                                "selectedTime": "15",
                                "confirmed": false
                            }
                        ]
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
