from fastapi import Request
from fastapi import APIRouter
from api_fast_api import templates
from fastapi.responses import HTMLResponse
from api_fast_api.models import select_lessons_by_month

# Создаем экземпляр APIRouter с префиксом
router_admin = APIRouter(prefix="/api_admin")


# Маршрут регистрации
@router_admin.post("/registration")
async def register_user(request: Request):
    """
    В разработке !!!
    """
    ...
    return {"msg": "Registration new user ok", "status": 200}


# Маршрут авторизации пользователя
@router_admin.post("/login")
async def login_user():
    """
    В разработке !!!
    """
    ...
    return {"message": "User login"}


# Маршрут выхода пользователя
@router_admin.post("/logout")
async def logout_user():
    """
    В разработке !!!
    """
    ...
    return {"message": "User logout"}


# Маршрут забронированных дней в календаре
@router_admin.get("/selection_classes_calendar/{date_in}")
async def get_selection_classes_calendar(date_in: str):
    """
    Получить данные календаря для указанной даты.\n
    Выборка идет опираясь на год-месяц
    date_in: Строка в формате YYYY-M-DD.\n
    return: {2024-4-24: 'true', 2024-4-30: 'await'}\n
    true - дата одобрена
    await - дата в ожидании
    """
    # Получаем статус и список
    status, list_days_month = select_lessons_by_month(date_in)
    if status == 500:
        return {status: list_days_month}  # {'200': results_dict_sorted}

    return list_days_month


# Маршрут на страницы авторизации пользователя
@router_admin.get("/form_auth", response_class=HTMLResponse)
async def read_form_auth():
    """
    Тестируется !!!
    """
    test_variable = "Текст из тестовой переменной"
    return templates.TemplateResponse(name="admin.html", context={"test_variable": test_variable}
    )
