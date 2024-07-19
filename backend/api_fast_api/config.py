# Файл конфигурации приложения
import os
import secrets
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

# Список разрешенных адресов
ORIGINS = os.getenv('ALLOWED_ORIGINS').split(',')

# Секретный ключ (автоматическая генерация)
SECRET_KEY = secrets.token_hex(32)

# Главная директория расположения проекта
ROOT_DIR = ...

# Получаем абсолютный путь к базовой папке проекта
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Подключение к базе данных SQLite
SQLALCHEMY_DATABASE_URL = 'sqlite:///' + os.path.join(BASE_DIR, 'db_api', 'async_api_data.db')

# Подключение к АССИНХРОННОЙ базе данных SQLite
ASYNC_SQLALCHEMY_DATABASE_URL = 'sqlite+aiosqlite:///' + os.path.join(BASE_DIR, 'db_api', 'async_api_data.db')

# Путь к папке статических файлов static
STATIC_FOLDER_PATH = os.path.join(BASE_DIR, 'static')
# Путь к папке с шаблонами html(jinja2)
TEMPLATES_FOLDER_PATH = os.path.join(BASE_DIR, 'templates')

# Время жизни токена
ACCESS_TOKEN_EXPIRE_MINUTES = 60
# Алгоритм кодирования
ALGORITHM = os.environ.get('ALGORITHM')
