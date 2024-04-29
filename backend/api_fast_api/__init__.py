from fastapi import FastAPI
from .models import create_database
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from api_fast_api.routes_admin import router_admin
from api_fast_api.routes_calendar import router_calendar
from api_fast_api.config import ORIGINS, STATIC_FOLDER_PATH

# Создаем экземпляр FastAPI приложения
app = FastAPI()

# Подключаем маршруты из APIRouter
app.include_router(router_admin)
app.include_router(router_calendar)

# Подключаем статические файлы из папки "static"
app.mount("/static", StaticFiles(directory=STATIC_FOLDER_PATH), name="static")

#
# Путь к директории с шаблонами
templates = Jinja2Templates(directory="templates")

# Добавляем CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin", "Authorization"],
)

# Создаем БД если ее нет
create_database()
