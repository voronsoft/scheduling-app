from datetime import datetime
from fastapi import Request

from api_fast_api.models.asinc_models import async_get_lessons_for_day


# ======================== Функция генерации карточек уроков пользователей
async def async_generating_user_lesson_cards(in_users_data_list):
    """Функция генерации карточек уроков пользователей

    :param in_users_data_list (list[dict,])

    :return str()
    """
    # Создаем пустой список для хранения карточек
    cards = str()

    # Проходимся по каждому словарю с данными пользователя
    for user in in_users_data_list:
        print("666 ", user)
        # Создаем HTML-разметку карточки
        card_content = f"""
            <div class="card {'text-bg-success' if user['confirmed'] else 'text-bg-danger'} mt-3"">
                <h5 class="card-header">{user['firstName']} {user['lastName']}</h5>
                <div class="card-body">
                    <p class="card-text">
                        <p class="card-text">Phone: {user['phone']}</p>
                        <p class="card-text">Email: {user['email']}</p>
                        <p class="card-text">Date: {user['selected_date']}</p>
                        <p class="card-text">Time: {user['selectedTime']}</p>
                        <p class="card-text">Confirmed: {user['confirmed']}</p> 
                    </p>
                </div>
                <div class="card-footer">
                    <button type="button" onclick="changeLessonStatus({user['id']})" class="btn btn-success" data-bs-dismiss="modal" {'disabled' if user['confirmed'] else ''}>Confirmed</button>
                    <button type="button" onclick="deleteLesson({user['id']})" class="btn btn-danger" data-bs-dismiss="modal">Delete</button>
                </div>
            </div>
            
        """
        cards += card_content
    # Возвращаем список карточек
    # print(cards)
    return cards


# TODO нужно продумать логику если в одном дне несколько записей...как красить фон и так далее
# ======================== Функция для текущего года и текущего месяца.
async def async_generate_calendar(date_dict: dict, year: int, month: int) -> str:
    """
    Функция генерации календаря по датам которые зарезервированы под уроки
    :param date_dict: {'2024-05-12': True, '2024-05-13': False, '2024-05-22': True}
    :param year: int
    :param month: int
    :return: str(html cod)
    """
    print("444a",date_dict)
    # Определяем первый день месяца
    first_day_of_month = datetime(year, month, 1)

    # Определяем количество дней в месяце
    if month == 12:
        days_in_month = (datetime(year + 1, 1, 1) - first_day_of_month).days
    else:
        days_in_month = (datetime(year, month + 1, 1) - first_day_of_month).days

    # Определяем дни недели для первого дня месяца
    start_day_of_week = first_day_of_month.weekday()

    # Начинаем формирование HTML для календаря
    calendar_html = f'''
        <h4>{first_day_of_month.strftime("%B %Y")}</h4>
        <table class="table table-bordered id="tbl-cldr">

                <tr>
                    <th class="table-light text-center">Mon</th>
                    <th class="table-light text-center">Tue</th>
                    <th class="table-light text-center">Wed</th>
                    <th class="table-light text-center">Thu</th>
                    <th class="table-light text-center">Fri</th>
                    <th class="table-danger text-center">Sat</th>
                    <th class="table-danger text-center">Sun</th>
                </tr>

            <tbody>
    '''

    # Заполняем календарь
    calendar_html += '<tr>'
    for i in range(start_day_of_week):
        calendar_html += '<td></td>'

    for day in range(1, days_in_month + 1):
        current_day = datetime(year, month, day)
        cell_style = ''
        modal_id = f'modal-{day}'
        # Если дата есть в списке
        if current_day.strftime('%Y-%m-%d') in date_dict:
            # Получаем данные об уроке/уроках
            sts, lessons = await async_get_lessons_for_day(current_day.strftime('%Y-%m-%d'))
            print("555lessons", lessons)
            # Генерируем карточки уроков пользователей
            get_card_html = await async_generating_user_lesson_cards(lessons)
            bg_style = ""
            # Проверяем значение метки (одобрено:True, ожидает:False)
            if date_dict[current_day.strftime('%Y-%m-%d')] is True:
                cell_style = 'text-success'  # отметка одобрено True
                bg_style = 'table-success'
            elif date_dict[current_day.strftime('%Y-%m-%d')] is False:
                cell_style = 'text-danger'  # отметка ожидает False
                bg_style = 'table-danger'

            calendar_html += f'''
                <td class="{bg_style} text-center">
                    <a href="#" class="text-decoration-none {cell_style}" data-bs-toggle="modal" data-bs-target="#{modal_id}"><b><h3>{day}</h3></b></a>
                    <div class="modal fade" id="{modal_id}" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                      <div class="modal-dialog modal-dialog-scrollable">
                        <div class="modal-content">
                          <div class="modal-header">
                            <h5 class="modal-title" id="exampleModalLabel">{current_day.strftime('%Y-%m-%d')}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                          </div>
                          <div class="modal-body">
                            {get_card_html}
                          </div>
                          <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                          </div>
                        </div>
                      </div>
                    </div>
                </td>
            '''
        else:
            calendar_html += f'<td class="text-center">{day}</td>'

        if (start_day_of_week + day) % 7 == 0:
            calendar_html += '</tr><tr>'

    # Дополняем последний ряд до 7 дней, если необходимо
    while (start_day_of_week + days_in_month) % 7 != 0:
        calendar_html += '<td></td>'
        days_in_month += 1

    calendar_html += '</tr></tbody></table>'

    return calendar_html


# ======================== Функция для текущего года и текущего месяца.
def current_date() -> tuple:
    """
    Функция для текущего года и текущего месяца.

    Возвращает:
        current_date (str): Текущая полная дата в формате "ГГГГ-ММ-ДД".
        current_year (int): Текущий год.
        current_month (int): Текущий месяц.
    """
    # Получаем текущую дату и время
    now = datetime.now()

    # Получаем текущий год
    current_year = now.year

    # Получаем текущий месяц
    current_month = now.month

    # Возвращаем текущую дату в формате "ГГГГ-ММ-ДД"
    return current_year, current_month


# ======================== Функция проверки в запросе заголовок Authorization
def headers_scheck_auth(request: Request):
    """Функция проверки в запросе заголовок Authorization"""
    answer = False
    # Получаем все заголовки
    headers = request.headers

    # Проверяем наличие заголовка 'authorization'
    if 'authorization' in headers:
        # Получаем значение заголовка "Authorization" из запроса
        auth_header = request.headers.get('authorization')
        # Проверяем, что заголовок начинается с 'Bearer '
        if auth_header.startswith('Bearer '):
            # Извлекаем токен, отбросив 'Bearer ', и пробельные символы в начале строки
            token = auth_header[len('Bearer '):].strip()
            # В этой переменной 'token' у вас будет содержаться код токена
            answer = True

    return answer


# ======================== Функция получения даты на момент вызова функции
def date_at_the_time_the_function_was_called():
    """Функция генерации даты на момент вызова функции

    :return str 2024-05-24
    """
    date = datetime.now().date()
    return str(date)

