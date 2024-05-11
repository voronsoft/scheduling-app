from fastapi import Request
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend.api_fast_api.config import TEMPLATES_FOLDER_PATH
from backend.api_fast_api.func.functions import generate_calendar, current_date

# Создаем экземпляр APIRouter с префиксом
router_html = APIRouter(prefix="")

# Путь к директории с шаблонами (для рендеринга html страниц)
templates = Jinja2Templates(directory=TEMPLATES_FOLDER_PATH)


# ======================== Маршруты HTML страниц =========================
# Маршрут ГЛАВНОЙ страницы админпанели
@router_html.get("/admin", response_class=HTMLResponse, include_in_schema=False)
async def html_index(request: Request):
    """ В разработке !!! """

    user_group = 1  # группа пользователя 1 админ, 0 посторонний
    user = "admin"  # тестовая переменная
    # Получаем список зарезервированных дат из БД
    dict_days = {}
    # Получаем дату для генерации календаря
    year, month = current_date()

    calendar = generate_calendar(dict_days, year, month)

    return templates.TemplateResponse(request=request, name="index.html", context={"user_group": user_group, "user_name": user, "calendar": calendar})


# Маршрут РЕГИСТРАЦИИ пользователя
@router_html.get("/registration", response_class=HTMLResponse, include_in_schema=False)
async def html_registration(request: Request):
    """
    В разработке !!!
    """
    title = "Registration user"
    return templates.TemplateResponse(request=request, name="registration.html", context={"title": title})


# Маршрут АВТОРИЗАЦИИ пользователя
@router_html.get("/authorization", response_class=HTMLResponse, include_in_schema=False)
async def html_authorization(request: Request):
    """
    В разработке !!!
    """
    title = "Registration user"
    return templates.TemplateResponse(request=request, name="authorization.html", context={"title": title})

# ======================== Маршруты HTML страниц =========================
