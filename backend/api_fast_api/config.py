# Файл конфигурации приложения
import os
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

# Список разрешенных адресов
ORIGINS = os.getenv('ALLOWED_ORIGINS').split(',')

# Секретный ключ
SECRET_KEY = os.environ.get('SECRET_KEY')

# Получаем абсолютный путь к корню сайта
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Подключение к базе данных SQLite
SQLALCHEMY_DATABASE_URL = 'sqlite:///' + os.path.join(BASE_DIR, 'db_api', 'api_data.db')

# Путь к папке статических файлов static
STATIC_FOLDER_PATH = os.path.join(BASE_DIR, 'static')
# Путь к папке с шаблонами html(jinja2)
TEMPLATES_FOLDER_PATH = os.path.join(BASE_DIR, 'templates')


if __name__ == "__main__":
    print("ORIGINS", ORIGINS)
    print("SECRET_KEY", SECRET_KEY)
    print('BASE_DIR', BASE_DIR)
    print('SQLALCHEMY_DATABASE_URI', SQLALCHEMY_DATABASE_URL)
    print('STATIC_FOLDER_PATH', STATIC_FOLDER_PATH)
    print('TEMPLATES_FOLDER_PATH', TEMPLATES_FOLDER_PATH)