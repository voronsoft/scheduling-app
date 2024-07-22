from typing import Annotated
from datetime import timedelta

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, Request, Response, status, HTTPException

from api_fast_api.config import ACCESS_TOKEN_EXPIRE_MINUTES
from api_fast_api.auth.authentication import (create_access_token, authenticate_user, get_password_hash, oauth2_scheme,
                                              validate_token
                                              )
from api_fast_api.models.asinc_models import (async_change_lesson_data_db, async_get_lesson_data_db,
                                              async_delete_lesson_db, async_get_lessons_for_month,
                                              async_lesson_dates_for_the_month_db_frontend,
                                              async_lesson_dates_for_the_month_db_backend, async_save_user_registration
                                              )
from api_fast_api.models.models_pydantic import RegistrationUserPydantic, TokenPydantic, UpdateLessonDataPydantic


router_admin = APIRouter(prefix="/api_admin")  # Создаем экземпляр APIRouter с префиксом
tags_metadata_admin = [{"name": "ADMINpanel", "description": "Маршруты админ панели"}, ]


# ======================== Маршрут регистрации пользователя ========================
@router_admin.post("/registration", include_in_schema=True, tags=["ADMINpanel"])
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

    # # Хешируем полученный пароль из запроса на регистрацию
    # hashed_password = get_password_hash(password)
    # Хешируем полученный пароль из запроса на регистрацию
    hashed_password = await get_password_hash(password)  # Вызов асинхронной функции
    print("=====hashed_password", hashed_password)

    # Передаем данные в функцию для записи нового пользователя в БД
    sts, result = await async_save_user_registration(username, email, hashed_password)
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
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 request: Request
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
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"}, )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return TokenPydantic(access_token=access_token, token_type="bearer")


# ======================== Маршрут получение списка ДАТ уроков на запрашиваемый месяц ========================
@router_admin.get("/lesson_dates_for_the_month_backend/{date_month}",
                  include_in_schema=False,
                  tags=["ADMINpanel"],
                  status_code=200
                  )
async def get_lesson_dates_for_the_month_backend(date_month: str, response: Response):
    """
    **Метод GET**

    **Маршрут получение списка дат уроков на запрашиваемый месяц (внутренняя админ панель)**
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
    - http://example.com/api_admin/lesson_dates_for_the_month_backend/2024-9-24
    - http://example.com/api_admin/lesson_dates_for_the_month_backend/2024-09-24

    Пример ответа:
    - 200: {"2024-4-24": True,"2024-4-30": False}
    - 404: {"Not found"} Даты на этот месяц не найдены.
    - 422:{"detail": "Invalid date format"}
    - 500:{"detail": "Internal Server Error: Something went wrong"}
    """

    sts, result = await async_lesson_dates_for_the_month_db_backend(date_month)

    if sts == 200:
        response.status_code = status.HTTP_200_OK
        return result
    elif sts == 404:
        response.status_code = status.HTTP_404_NOT_FOUND
        return result
    elif sts == 422:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return result
    elif sts == 500:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return result


@router_admin.get("/lesson_dates_for_the_month_frontend/{date_month}",
                  include_in_schema=True,
                  tags=["ADMINpanel"],
                  status_code=200
                  )
async def get_lesson_dates_for_the_month_frontend(date_month: str, response: Response):
    """
    **Метод GET**

    **Маршрут получение списка дат уроков на запрашиваемый месяц (фронтенд админ панель)**
    Параметры:
    - date_in: Дата в формате YYYY-MM-DD. 2024-04-27

    Возвращаемые данные:
    -

    Возможные статусы ответа:
    - 200: Успешный запрос. Возвращается словарь с данными о бронировании.
    - 404: Даты занятий не найдены в бд на запрашиваемый месяц
    - 422: Некорректный формат даты. Возвращается детальное описание ошибки.
    - 500: Внутренняя ошибка сервера. Возвращается описание ошибки.

    Примеры использования:
    - http://example.com/api_admin/lesson_dates_for_the_month_frontend/2024-9-24
    - http://example.com/api_admin/lesson_dates_for_the_month_frontend/2024-09-24

    Пример ответа:
    - 200: data
    - 404: {"Not found"} Даты на этот месяц не найдены.
    - 422:{"detail": "Invalid date format"}
    - 500:{"detail": "Internal Server Error: Something went wrong"}
    """

    sts, result = await async_lesson_dates_for_the_month_db_frontend(date_month)

    if sts == 200:
        response.status_code = status.HTTP_200_OK
        return result
    elif sts == 404:
        response.status_code = status.HTTP_404_NOT_FOUND
        return result
    elif sts == 422:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return result
    elif sts == 500:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return result


# ======================== Маршрут получения занятий на запрашиваемый месяц ========================
# ========================               (полные данные)                    ========================
@router_admin.get("/get_lessons_for_a_month/{date_y_m_d}", tags=["ADMINpanel"], status_code=200)
async def get_lessons_for_a_month(date_y_m_d: str, response: Response, token: Annotated[str, Depends(oauth2_scheme)]):
    """
    **Метод GET - Endpoint protected**

    **Маршрут получения занятий на запрашиваемый месяц (полные данные о заявке)**

    Параметры принимает:
    - date_in: Дата в формате YYYY-MM-DD. Тип строка. (2024-06-16)

    Возвращаемые данные:
    - Словарь с данными о бронировании на указанную дату месяца.

            [
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

                [
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

    - 404:{"lessons": "Not found"}

    - 422: {"detail": "Invalid date format"}

    - 500: {"detail": error description}
    """

    if not validate_token(str(token)):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'message': 'Not authenticated'}

    # Запрашиваем из БД список занятий
    sts, result = await async_get_lessons_for_month(date_y_m_d)
    if sts == 200:
        response.status_code = status.HTTP_200_OK
        return result
    elif sts == 404:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message': 'Not found'}
    elif sts == 422:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return result
    elif sts == 500:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'message': result}


# ======================== Маршрут УДАЛЕНИЯ ЗАПИСИ О УРОКЕ =========================
# TODO добавить документацию
@router_admin.delete("/delete_lesson_frontend/{lesson_id}", include_in_schema=True, tags=["ADMINpanel"])
async def deleting_a_lesson_frontend(lesson_id: int, response: Response, token: Annotated[str, Depends(oauth2_scheme)]):
    """
    **Метод DELETE - Endpoint protected**

    **Удаление записи урока из бд**

    Ссылка для запроса:

    - http://example.com/api_admin/delete_lesson_frontend/10

    Варианты ответов:

    - 200 {'message': 'Lesson delete successfully.'}
    - 404 {'message': 'Not found'}
    - 500 {'message': 'Error server'}
    """
    print("token: ", token)

    if not validate_token(str(token)):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'message': 'Not authenticated'}

    # Вызываем функцию для удаления записи урока
    sts, result = await async_delete_lesson_db(lesson_id)

    # Проверяем результат выполнения функции
    if sts == 200:
        # Если операция выполнена успешно, возвращаем HTTP-статус 200 (OK)
        response.status_code = status.HTTP_200_OK
        return {'message': 'Lesson delete successfully.'}
    elif sts == 404:
        # Если не найдено урока в бд
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message': 'Not found'}
    elif sts == 500:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'message': result}


# ======================== Маршрут изменения данных в записи урока =========================
# TODO добавить документацию
@router_admin.patch("/change_lesson_data/{lesson_id}", include_in_schema=True, tags=["ADMINpanel"])
async def change_lesson_data(lesson_id: int,
                             lesson_data: UpdateLessonDataPydantic,
                             response: Response,
                             request: Request,
                             token: Annotated[str, Depends(oauth2_scheme)]
                             ):
    """
    **Метод PATH - Endpoint protected**

    **Изменение данных в записи урока**

    Принимает id записи как параметр пути.
    - http://example.com/api_admin/change_lesson_data/10

    А в POST запросе передается json c названием полей которые будут изменены

        {
            username: str,
            last_name: str,
            phone: str,
            email: str,
            selected_date: str,
            time: str,
            confirmed: str,
        }

    Варианты ответов:

    - 200 {'message': 'Lesson update data successfully.'}
    - 400 {'message': 'Invalid date format - 22100-01-100'}
    - 404 {'message': 'Not found lesson'}
    - 500 {'message': 'Error server'}
    """

    if not validate_token(str(token)):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'message': 'Not authenticated'}

    request_data = dict(lesson_data)  # Получаем данные JSON из запроса
    print("request_data: ", request_data)

    # Вызываем функцию для изменения данных урока
    sts, result = await async_change_lesson_data_db(lesson_id, request_data)

    # Проверяем результат выполнения функции
    if sts == 200:
        # Если операция выполнена успешно, возвращаем HTTP-статус 200 (OK)
        response.status_code = status.HTTP_200_OK
        return {'message': 'Lesson update data successfully.'}
    elif sts == 400:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': result}
    elif sts == 404:
        # Если не найдено урока в бд
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message': 'Not found lesson'}
    elif sts == 500:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'message': result}


# ======================== Маршрут получения данных записи урока по id =========================
@router_admin.get("/get_lesson_data/{lesson_id}", include_in_schema=True, tags=["ADMINpanel"])
async def get_lesson_data_frontend(lesson_id: int,
                                   response: Response,
                                   token: Annotated[str, Depends(oauth2_scheme)]
                                   ):
    """
    **Метод GET - Endpoint protected**

    **Маршрут получения данных записи урока по id**

    Принимает id записи как параметр пути.
    - http://example.com/api_admin/get_lesson_data/10

    Варианты ответов:

    - 200 {'username': 'Jon Doe', "phone": "123456789", ...}
    - 404 {'message': 'Not found lesson'}
    - 500 {'message': 'Error server'}
    """
    if not validate_token(str(token)):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'message': 'Not authenticated'}

    sts, result = await async_get_lesson_data_db(lesson_id)

    # Проверяем результат выполнения функции
    if sts == 200:
        # Если операция выполнена успешно, возвращаем HTTP-статус 200 (OK)
        response.status_code = status.HTTP_200_OK
        return result
    elif sts == 404:
        # Если не найдено урока в бд
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message': 'Not found lesson'}
    elif sts == 500:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'message': result}
