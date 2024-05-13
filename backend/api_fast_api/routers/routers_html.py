from asyncio import sleep
from typing import Annotated

from fastapi import Request, APIRouter, Depends, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from backend.api_fast_api.auth.authentication import get_current_user, oauth2_scheme
from backend.api_fast_api.config import TEMPLATES_FOLDER_PATH
from backend.api_fast_api.func.functions import generate_calendar, current_date, headers_scheck_auth, date_at_the_time_the_function_was_called
from backend.api_fast_api.models.models_pydantic import UserPydantic
from backend.api_fast_api.models.models_sql import lesson_dates_for_the_month_db

# Создаем экземпляр APIRouter с префиксом
router_html = APIRouter(prefix="")

# Путь к директории с шаблонами (для рендеринга html страниц)
templates = Jinja2Templates(directory=TEMPLATES_FOLDER_PATH)


# ======================== Маршруты АДМИНПАНЕЛЬ get =========================

@router_html.get("/admin", response_class=HTMLResponse, include_in_schema=False, tags=["ADMINpanelHTML"])
async def html_index_get(request: Request):
# async def html_index_get(request: Request, token: Annotated[str, Depends(oauth2_scheme)]):
    """ В разработке !!! """

    user_group = 1  # Группа пользователя: 1 админ, 0 посторонний
    user = "admin"  # Имя пользователя
    # TODO необходимо доделать автоматическую генерацию отмеченных дней из БД
    # Получаем дату в момент вызова функции
    data = date_at_the_time_the_function_was_called()
    # Получаем список зарезервированных дат из БД на текущий месяц
    dict_days = lesson_dates_for_the_month_db(data)[1]
    print("dict_days", dict_days)
    # Получаем дату для генерации календаря (дата формируется на момент вызова кода)
    year, month, _ = map(int, data.split("-"))
    # Генерируем календарь передав: 1 список занятий из БД / 2 год / 3 месяц
    calendar = generate_calendar(dict_days, year, month)

    return templates.TemplateResponse(request=request, name="index.html", context={"user_group": user_group, "user_name": user, "calendar": calendar})


# ======================== Маршрут РЕГИСТРАЦИИ пользователя =========================
@router_html.get("/registration", response_class=HTMLResponse, include_in_schema=False, tags=["ADMINpanelHTML"])
async def html_registration(request: Request):
    """
    В разработке !!!
    """
    title = "Registration user"
    return templates.TemplateResponse(request=request, name="registration.html", context={"title": title})


# ======================== Маршрут АВТОРИЗАЦИИ пользователя get =========================
# Маршрут АВТОРИЗАЦИИ пользователя
@router_html.get("/authorization", response_class=HTMLResponse, include_in_schema=False, tags=["ADMINpanelHTML"])
async def html_authorization_get(request: Request):
    """
    В разработке !!!
    """
    title = "Authentication/Login user"
    return templates.TemplateResponse(request=request, name="authorization.html", context={"title": title})


# ======================== Маршрут ОБРАБОТКИ ОТВЕТОВ СЕРВЕРА =========================
@router_html.post("/proc-serv-resp", include_in_schema=False, tags=["ADMINpanelHTML"])
async def processing_server_responses(request: Request, response: Response):
    """
    В разработке !!!
    """
    # Получаем данные из тела запроса в формате формы HTML
    data = await request.json()
    # Вытягиваем данные из запроса
    status_code = data["status"]  # Статус код ответа
    data_body_request = data["detail"]  # Данные из тела ответа

    print("(post 'proc-serv-resp') Получен ответ от сервера\n", data)
    print("status_code: ", status_code)
    print("data_body_request: ", data_body_request)

    return RedirectResponse('/test')


# ======================== Маршрут TEST =========================
@router_html.post("/test", response_class=HTMLResponse, include_in_schema=False, tags=["ADMINpanelHTML"])
@router_html.get("/test", response_class=HTMLResponse, include_in_schema=False, tags=["ADMINpanelHTML"])
async def html_test(request: Request):
    title = "Страница ошибок"
    error = request.json()
    return templates.TemplateResponse(request=request, name="test.html", context={"error": error, "title": title})
