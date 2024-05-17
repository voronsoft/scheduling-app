import requests


def send_post_request():
    # URL адрес вашего сервера, куда будет отправлен POST запрос
    url = "http://127.0.0.10:8888/error"

    # JSON данные для отправки
    data = {
        "error_message": "Текст сообщения об ошибке"
    }

    try:
        # Отправляем POST запрос
        response = requests.post(url, json=data)

        # Проверяем статус ответа
        if response.status_code == 200:
            print("Запрос успешно выполнен.")
        else:
            print(f"Произошла ошибка. Код статуса: {response.status_code}")
    except Exception as e:
        print(f"Произошла ошибка при выполнении запроса: {e}")


if __name__ == "__main__":
    # Вызываем функцию для отправки POST запроса
    send_post_request()
