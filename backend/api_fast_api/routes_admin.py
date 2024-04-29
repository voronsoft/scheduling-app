from fastapi import Request
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from backend.api_fast_api.config import TEMPLATES_FOLDER_PATH
from backend.api_fast_api.models import select_lessons_by_month

# Создаем экземпляр APIRouter с префиксом
router_admin = APIRouter(prefix="/api_admin")

# Путь к директории с шаблонами (для рендеринга html страниц)
templates = Jinja2Templates(directory=TEMPLATES_FOLDER_PATH)


# Маршрут регистрации
@router_admin.post("/registration")
async def register_user(request: Request):
    """
    В разработке !!!

    Принимает:

    username: str

    email: str

    password: str

    Возвращает: json

    {status: status, message: message,}
    """
    ...
    return {"status": "status", "message": "Registration new user ok"}


# Маршрут авторизации пользователя
@router_admin.post("/authorization")
async def authorization_user(request: Request):
    """
    В разработке !!!

    Принимает:

    username: str

    email: str

    password: str

    Возвращает: json

    {status: token, }
    """
    ...
    return {"status": "status", "message": "message", }


# Маршрут выхода пользователя
@router_admin.post("/logout")
async def logout_user():
    """
    В разработке !!!

    Принимает:

    token: str

    flag: False or True (str)

    Возвращает: json

    {status: status, message: message}
    """
    ...
    return {"status": "status", "message": "User logout"}


# Маршрут забронированных дней в календаре
@router_admin.get("/selection_classes_calendar/{date_in}")
async def get_selection_classes_calendar(date_in: str):
    """
    Получить данные календаря для указанной даты.

    Выборка идет опираясь на год-месяц

    date_in: Строка в формате YYYY-M-DD.

    return: dict {"status": status, "list_days": {2024-4-24: 'true', 2024-4-30: 'await'}}

    true - дата одобрена / await - дата в ожидании
    """
    # Получаем код статуса и список
    status, dict_days_month = select_lessons_by_month(date_in)
    if status == 500:
        return {"status": status, "list_days": dict_days_month}

    return dict_days_month
