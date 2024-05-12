import requests


def make_request():
    url = "http://127.0.0.10:8888/admin"
    headers = {
        "Authorization": "Hello pipi"
    }

    response = requests.get(url, headers=headers)

    return response


response = make_request()
print(response.status_code)
print(response.text)
