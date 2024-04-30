from datetime import datetime, timedelta


# Функция генерации календарного месяца в админ панели
def generate_calendar(date_dict: dict, year: int, month: int) -> str:
    """
    Функция генерации календаря по датам которые зарезервированы под уроки
    :param date_dict: dict
    :param year: int
    :param month: int
    :return: str(html cod)
    """
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
    <div class="container">
        <h2>Календарь на {first_day_of_month.strftime("%B %Y")}</h2>
        <table class="table table-bordered">
            <thead>
                <tr>
                    <th>Пн</th>
                    <th>Вт</th>
                    <th>Ср</th>
                    <th>Чт</th>
                    <th>Пт</th>
                    <th>Сб</th>
                    <th>Вс</th>
                </tr>
            </thead>
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
        if current_day.strftime('%Y-%m-%d') in date_dict:
            if date_dict[current_day.strftime('%Y-%m-%d')] == 'true':
                cell_style = 'btn-success'
            elif date_dict[current_day.strftime('%Y-%m-%d')] == 'await':
                cell_style = 'btn-primary'
            calendar_html += f'''
                <td>
                    <button type="button" class="btn {cell_style}" data-bs-toggle="modal" data-bs-target="#{modal_id}">
                        {day}
                    </button>
                    <div class="modal fade" id="{modal_id}" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                      <div class="modal-dialog">
                        <div class="modal-content">
                          <div class="modal-header">
                            <h5 class="modal-title" id="exampleModalLabel">Дата {current_day.strftime('%Y-%m-%d')}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                          </div>
                          <div class="modal-body">
                            <p>Данные пользователя из бд</p>
                          </div>
                          <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                          </div>
                        </div>
                      </div>
                    </div>
                </td>
            '''
        else:
            calendar_html += f'<td>{day}</td>'

        if (start_day_of_week + day) % 7 == 0:
            calendar_html += '</tr><tr>'

    # Дополняем последний ряд до 7 дней, если необходимо
    while (start_day_of_week + days_in_month) % 7 != 0:
        calendar_html += '<td></td>'
        days_in_month += 1

    calendar_html += '</tr></tbody></table></div>'

    return calendar_html


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

    # Получаем текущую дату в формате "ГГГГ-ММ-ДД"
    # current_date = now.strftime("%Y-%m-%d")
    # print(type(current_year), type(current_month))
    return current_year, current_month


if __name__ == "__main__":
    ...
    # # Пример использования функции
    # date_dict_test = {
    #     '2024-05-3': 'true',
    #     '2024-05-7': 'true',
    #     '2024-05-10': 'await',
    #     '2024-05-15': 'true',
    #     '2024-05-20': 'await',
    #     '2024-05-23': 'true',
    #     '2024-05-30': 'await',
    # }
    #
    # year_test = 2024
    # month_test = 5  # Май
    # calendar_html = generate_calendar(date_dict_test, year_test, month_test)
    # print(calendar_html)  # Это можно подставить в ваш HTML-шаблон
    print(current_date())
