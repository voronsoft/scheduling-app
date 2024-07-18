from fastapi import Request, APIRouter, Response, status, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates

from api_fast_api.auth.authentication import validate_token
from api_fast_api.config import TEMPLATES_FOLDER_PATH
from api_fast_api.func.csrf_functions import generate_csrf_token, checking_csrf_token
from api_fast_api.func.functions import date_at_the_time_the_function_was_called, async_generate_calendar
from api_fast_api.models.asinc_models import (async_lesson_dates_for_the_month_db_backend,
                                              async_get_lessons_for_month_one_dimensional_list,
                                              async_change_lesson_status_db, async_delete_lesson_db
                                              )
from api_fast_api.routers.routes_admin import login_for_access_token

# Создаем экземпляр APIRouter с префиксом
router_html = APIRouter(prefix="")

# Путь с шаблонами (для рендеринга html страниц)
templates = Jinja2Templates(directory=TEMPLATES_FOLDER_PATH)


# TODO Добавить описание
# ======================== Маршруты АДМИНПАНЕЛЬ get =========================
@router_html.get("/admin", response_class=HTMLResponse, include_in_schema=False, tags=["ADMINpanelHTML"])
async def html_index_get(request: Request):
    """ В разработке !!! """
    print("Пришел запрос в /admin GET")

    # Проверяем есть ли JWT токен в сессии
    if "jwt_token" in request.session:
        print("Раздел - Проверяем есть ли JWT токен в сессии")
        # Извлекаем данные из сессии
        jwt_data = request.session["jwt_token"]
        access_token = jwt_data.get("access_token")
        token_type = jwt_data.get("token_type")
        # Проверка jwt токена и метода шифрования
        if token_type == "bearer" and validate_token(access_token):
            print("Раздел - Проверка jwt токена и метода шифрования")
            # Сохраняем JWT токен и тип токена в сессии
            request.session["jwt_token"] = {"token_type": token_type, "access_token": access_token}

            user_group = 1  # Группа пользователя: 1 админ, 0 посторонний
            user = "Admin"  # Имя пользователя

            # Получаем дату в момент вызова функции
            crnt_date = date_at_the_time_the_function_was_called()
            print("111======= ",crnt_date)

            # Получаем список зарезервированных дат из БД на текущий месяц
            # lst_date_lesns = lesson_dates_for_the_month_db_backend(crnt_date)[1]
            lst_date_lesns = await async_lesson_dates_for_the_month_db_backend(crnt_date)
            lst_date_lesns = lst_date_lesns[1]
            print("444lst_date_lesns", lst_date_lesns)


            # Получаем дату для генерации календаря (дата формируется на момент вызова кода)
            year, month, _ = map(int, crnt_date.split("-"))
            # Генерируем календарь передав: 1 список занятий / 2 год / 3 месяц
            calendar = await async_generate_calendar(lst_date_lesns, year, month)

            # Получаем список занятий на месяц с полными данными в одномерный словарь
            # _, list_data_lessons = get_lessons_for_month_one_dimensional_list(crnt_date)
            _, list_data_lessons = await async_get_lessons_for_month_one_dimensional_list(crnt_date)

            response = templates.TemplateResponse(request=request,
                                                  name="index.html",
                                                  context={
                                                          "user_group": user_group,
                                                          "user_name": user,
                                                          "calendar": calendar,
                                                          "list_data_lessons": list_data_lessons,
                                                  }
                                                  )
            print("Раздел - Этап вывода шаблона")
            return response

        # Если токен найден, но не прошел проверку (допустим прошлый токен или подделка)
        # перенаправляем пользователя на страницу авторизации.
        else:
            print("Раздел - Токен не прошел проверку !!!")
            return await html_login_get(request, error_message="Токен не прошел проверку !!!")

    else:
        # Если токен отсутствует, перенаправляем пользователя на страницу авторизации
        print("JWT не найден перенаправляем в /login")
        # Перенаправляем в /admin
        return RedirectResponse(url="/login", status_code=303)


# ======================== Маршрут АВТОРИЗАЦИИ пользователя GET/POST =========================
# TODO добавить документацию
@router_html.get("/login", response_class=HTMLResponse, include_in_schema=False, tags=["ADMINpanelHTML"])
async def html_login_get(request: Request, error_message: str = None):
    """
    GET - Маршрут авторизации пользователя.
    """
    error_message = error_message
    print("Пришел запрос в login GET")
    title = "Login user"
    # Генерируем CSRF токен
    csrf_token = generate_csrf_token()
    # Сохраняем токен в сессии
    request.session["csrf_token"] = csrf_token

    response = templates.TemplateResponse(request=request,
                                          name="login.html",
                                          context={
                                                  "title": title,
                                                  "csrf_token": csrf_token,
                                                  "error_message": error_message
                                          }
                                          )
    return response


# TODO добавить документацию
@router_html.post("/login", include_in_schema=False, tags=["ADMINpanelHTML"])
async def html_login_post(request: Request,
                          response: Response,
                          username: str = Form(...),
                          email: str = Form(...),
                          password: str = Form(...),
                          csrf_token: str = Form(...)
                          ):
    """
    POST - Маршрут проверки пользователя и получение токена
    """
    print("Пришел запрос в login POST")

    # Получаем CSRF токен из сессии
    session_csrf_token = request.session.get("csrf_token")

    # Если хоть один из токенов None обнуляем оба токена
    if (not session_csrf_token and csrf_token) or (session_csrf_token and not csrf_token):
        print("Один из токенов был пуст ОШИБКА !!!")
        # Очищаем оба токена
        request.session.pop("csrf_token", None)
        csrf_token = None
    # Если CSRF токены не совпадают, перенаправляем пользователя на страницу авторизации.
    elif not checking_csrf_token(session_csrf_token, csrf_token):
        print("CSRF токены НЕ СОВПАДАЮТ ОШИБКА !!!")
        # Очищаем оба токена
        request.session.pop("csrf_token", None)
        csrf_token = None
    # Если CSRF токен прошел проверку, создаем(получаем) JWT токен
    else:
        print("Токены CSRF совпадают")
        # Очищаем токены CSRF после проверки, предотвращая повторное использование
        request.session.pop("csrf_token", None)
        csrf_token = None

        # Создаем экземпляр OAuth2PasswordRequestForm, содержащий данные пользователя
        form_data = OAuth2PasswordRequestForm(username=username, password=password)
        # JWT - Вызываем маршрут для авторизации и получения токена JWT
        try:
            token = await login_for_access_token(form_data=form_data, request=request)
            # Сохраняем JWT токен в сессию, перенаправляем в маршрут главной страницы /admin
            access_token = token.access_token
            token_type = token.token_type
            # Сохраняем JWT токен и тип токена в сессии
            request.session["jwt_token"] = {"token_type": token_type, "access_token": access_token}

            # Перенаправляем в /admin
            return RedirectResponse(url="/admin", status_code=303)

        except Exception as e:
            print("!! ОШИБКА JWT недействителен: ", str(e))
            return await html_login_get(request, error_message="Неверное имя пользователя или пароль")

    return RedirectResponse(url="/login", status_code=303)


# ======================== Маршрут РЕГИСТРАЦИИ пользователя =========================
# TODO добавить документацию
@router_html.get("/registration", response_class=HTMLResponse, include_in_schema=False, tags=["ADMINpanelHTML"])
async def html_registration(request: Request):
    """
    В разработке !!!
    """
    title = "Registration user"
    return templates.TemplateResponse(request=request, name="registration.html", context={"title": title})


# ======================== Маршрут ИЗМЕНЕНИЯ СТАТУСА УРОКА =========================
@router_html.post("/change-lesson-status_backend", include_in_schema=False, tags=["ADMINpanelHTML"])
async def change_lesson_status_backend(request: Request, response: Response):
    """
    Изменение статуса урока
    """
    request_body = await request.json()  # Получаем данные JSON из запроса
    lesson_id = request_body.get('lesson_id')  # Получаем значение lesson_id
    print("lesson_id=======lesson_id", lesson_id)

    # Вызываем функцию для изменения статуса урока
    sts, result = await async_change_lesson_status_db(lesson_id)

    # Проверяем результат выполнения функции
    if sts == 200:
        # Если операция выполнена успешно, возвращаем HTTP-статус 200 (OK)
        response.status_code = status.HTTP_200_OK
        return {'message': 'Lesson status changed successfully.'}
    elif sts == 404:
        # Если не найдено урока в бд
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message': 'Not found lesson'}
    elif sts == 500:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'message': result}

# ======================== Маршрут УДАЛЕНИЯ ЗАПИСИ О УРОКЕ =========================
# TODO добавить документацию
@router_html.delete("/delete-lesson_backend", include_in_schema=False, tags=["ADMINpanelHTML"])
async def deleting_a_lesson_backend(request: Request, response: Response):
    """
    Удаление записи урока из бд
    """

    request_body = await request.json()  # Получаем данные JSON из запроса
    lesson_id = request_body.get('lesson_id')  # Получаем значение lesson_id
    print("delete-lesson=======delete-lesson", lesson_id)

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
        return {'message': 'Not found lesson'}
    elif sts == 500:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'message': result}


# ======================== Маршрут ВЫХОДА ПОЛЬЗОВАТЕЛЯ post =========================
# TODO добавить документацию
@router_html.post("/logout", include_in_schema=False, tags=["ADMINpanel"])
async def logout_user(request: Request):
    """Маршрут выхода пользователя"""
    # Удаляем ключ "jwt_token" из сессии, если он существует
    request.session.pop("jwt_token", None)
    # Перенаправляем пользователя на страницу авторизации
    return RedirectResponse(url="/login", status_code=303)


# ======================== Маршрут ОБРАБОТКИ ОШИБОК GET/POST =========================
# TODO добавить документацию
@router_html.get("/error", response_class=HTMLResponse, include_in_schema=False, tags=["ADMINpanelHTML"])
async def html_error_get(request: Request, text_error: str = None):
    title = "Страница ошибок"
    # Заглушка
    error_message = text_error

    return templates.TemplateResponse(request=request,
                                      name="error_modal_window.html",
                                      context={"error_message": error_message, "title": title}
                                      )


# TODO добавить документацию
@router_html.post("/error", include_in_schema=False, tags=["ADMINpanelHTML"])
async def html_error_post(request: Request, response: Response):
    title = "Страница ошибок"
    # Получаем JSON-данные из тела запроса
    error_data = await request.json()
    # Получаем сообщение об ошибке из данных запроса
    error_message = error_data.get("error_message")
    # error_message = "(POST) Текст сообщения об ошибке"

    await html_error_get(request, error_data)
