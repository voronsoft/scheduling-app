import requests


# Пример запроса к защищенному маршруту
def resp_in_server(username: str = None, password: str = None):
    # URL маршрута для аутентификации
    authentication_route_url = 'http://127.0.0.10:8888/api_admin/authorization'
    # Данные для запроса аутентификации
    credentials = {
        'username': username,
        'password': password, }

    # Отправка POST-запроса для получения аутентификации
    response = requests.post(authentication_route_url, data=credentials)

    # Проверка успешности запроса
    if response.status_code == 200:
        # Вывод ответа в консоль
        print(f"Ответ от сервера пользователь найден: {response.status_code}\nТокен: {response.json()}")
    else:
        print("Ошибка при запросе аутентификации:", response.text)

    # URL защищенного маршрута создаем запрос с передачей значения даты
    # В запросе передаем данные о токене заголовке и все нужные данные для успешного ответа
    protected_route_url = 'http://127.0.0.10:8888/api_admin/get_lessons_for_a_month/'
    # Проверка успешности запроса на получение токена доступа
    if response.status_code == 200:
        # Извлечение токена из ответа сервера
        token = response.json()['access_token']

        # Создание заголовка авторизации с токеном
        headers = {'Authorization': f'Bearer {token}'}

        # Данные для отправки на защищенный эндпоинт
        data = '2024-05-16'

        # Отправка запроса на защищенный эндпоинт с правильным заголовком и токеном
        protected_route_response = requests.get(protected_route_url + data, headers=headers)

        # Проверка успешности запроса к защищенному маршруту
        if protected_route_response.status_code == 200:
            print("Запрос к защищенному маршруту выполнен успешно.")
            print(protected_route_response.json())
            return protected_route_response.json()
        else:
            print("Ошибка при запросе к защищенному маршруту:", protected_route_response.text)
    else:
        print("Ошибка при аутентификации:", response.text)


if __name__ == "__main__":
    resp_in_server("jon", "jon")
