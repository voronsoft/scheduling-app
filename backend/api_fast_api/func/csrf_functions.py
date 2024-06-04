import secrets


# ======================== Функция генерация CSRF токена
def generate_csrf_token() -> str:
    """
    Функция генерация CSRF токена
    :return: str(csrf_token)
    """
    csrf_token = secrets.token_hex(32)
    return csrf_token


# ======================== Функция проверка CSRF токена
def checking_csrf_token(session_csrf_token: str, csrf_token_form: str) -> bool:
    """
    Функция проверка CSRF токена

    :param - str(session_csrf_token) токен из сесии

    :param - str(csrf_token_form) токен из формы html

    :return bool
    """

    if session_csrf_token != csrf_token_form:
        return False
    else:
        return True
