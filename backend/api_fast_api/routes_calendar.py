from fastapi import Request
from fastapi import APIRouter
from api_fast_api.models import add_user_to_db

# Создаем экземпляр APIRouter с префиксом
router_calendar = APIRouter(prefix="/api_calendar")


# Маршрут прием данных с календаря
@router_calendar.post("/receiving-data-from-the-calendar")
async def receiving_data_calendar(request: Request):
    """
    Принимает параметры:\n
    firstName (str): Имя пользователя.\n
    lastName (str): Фамилия пользователя.\n
    email (str): Электронная почта пользователя.\n
    phone (str): Номер телефона пользователя.\n
    selectedDate (str): Выбранная дата пользователем. Тип 2024-2-27\n
    time (str): Выбранное время пользователем.\n
    """
    # Получаем JSON-данные из тела запроса
    user_data = await request.json()

    email = user_data.get('email')
    first_name = user_data.get('firstName')
    last_name = user_data.get('lastName')
    phone = user_data.get('phone')
    selected_date = user_data.get('selectedDate')
    selected_time = user_data.get('time')

    # Добавляем урок из календаря в БД
    status = add_user_to_db(first_name, last_name, email, phone, selected_date, selected_time)

    if not status[0]:
        return {"message": f"Application rejected user with this email: {email} already exists", "status": status[1]}

    return {"message": f"Application accepted!", "status": status[1]}

# -----------------------------------
