from fastapi import APIRouter, Response, status
from backend.api_fast_api.models.models_sql import add_lesson_data_to_db
from backend.api_fast_api.models.models_pydantic import ReceivingDataFromCalendarPydantic

# Создаем экземпляр APIRouter с префиксом
router_calendar = APIRouter(prefix="/api_calendar")

tags_metadata_calendar = [{"name": "CALENDAR", "description": "Маршруты для календаря"}, ]


# Маршрут приема заявок на уроки из компонента календарь.
@router_calendar.post("/receiving-data-from-the-calendar", tags=['CALENDAR'], status_code=200)
async def receiving_data_calendar(lesson_data: ReceivingDataFromCalendarPydantic, response: Response):
    """
    **Метод: POST**

    **Маршрут приема заявок на уроки из компонента календарь.**

    - Принимает:\n
            {
                "firstName": "Name",
                "lastName": "Last",
                "email": "user@example.com",
                "phone": "123456789",
                "selectedDate": "2024-02-20",
                "time": 14
            }

    Возможные статусы ответа:
    - 201: Успешный запрос. Возвращается словарь с данными о бронировании.
    - 409: Некорректный формат даты в запросе. Возвращается детальное описание ошибки.
    - 500: Внутренняя ошибка сервера. Возвращается описание ошибки.

    Пример ответа:

    - 201: {"message": "Application accepted!"}
    - 409: {"message": "This lesson already exists!"}
    - 500: {"message": description error}

    """
    status_code = add_lesson_data_to_db(
        lesson_data.name,
        lesson_data.surname,
        lesson_data.email,
        lesson_data.phone,
        lesson_data.selectedDate,
        lesson_data.time
    )

    if status_code is True:
        response.status_code = status.HTTP_201_CREATED
        return {"message": "Application accepted!"}
    elif status_code is False:
        response.status_code = status.HTTP_409_CONFLICT
        return {"message": "This lesson already exists!"}
    elif isinstance(status_code, dict):
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        print("status_code", status_code)
        return status_code
