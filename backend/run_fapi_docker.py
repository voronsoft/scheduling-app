"""Файл запуска приложения для docker"""

import uvicorn
import asyncio

from api_fast_api.logger_project.logger__app import logger_debug
from api_fast_api.models.async_models import async_create_database
from api_fast_api.func.create_project_structure_file import create_project_structure

if __name__ == "__main__":
    # Запускаем построение структуры папок и файлов в проекте
    create_project_structure()
    logger_debug.debug("Структура проекта успешно сохранена в файле.")

    # Создаем базу данных перед запуском приложения
    asyncio.run(async_create_database())

    logger_debug.debug("Проект запущен !")
    # Запускаем приложение по заданному адресу.
    uvicorn.run("api_fast_api:app", host="0.0.0.0", port=8888)
