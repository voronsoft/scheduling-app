import os
import asyncio
import aiofiles
import logging.config

from api_fast_api.config import LOG_DATA_PATH
from api_fast_api.logger_project.logger_config import logger_config


# ======================== Функция создания папки с файлами логгирования
async def creat_folder_log_data():
    """Функция создания папки с файлами логгирования"""

    # Проверяем существование папки для логов
    if not os.path.exists(LOG_DATA_PATH):
        print("Папка логов не найдена, СОЗДАНИЕ ПАПКИ ЛОГОВ")
        try:
            # Создаем папку для логов
            os.makedirs(LOG_DATA_PATH)
            # Создаем файлы для записи логов
            LOG_FILES = ['debug.log', 'warning.log', 'error.log']
            for log_file in LOG_FILES:
                # Используем aiofiles для асинхронного создания файлов
                async with aiofiles.open(os.path.join(LOG_DATA_PATH, log_file), 'w') as file:
                    await file.write('')  # Создаем пустой файл
        except Exception as e:
            print(f'Ошибка при создании папки для логов - {LOG_DATA_PATH}: {e}')
    else:
        print("Папка логов уже существует.")


async def main():
    await creat_folder_log_data()

# 1 -шаг
# Так как логгер загружается первым в приложении.
# Для его корректной работы нужно создать папку logs_data для запуска конфигурации.
# Запускаем функцию для создания папки логов.
asyncio.run(main())

# 2 -шаг
# Задаем конфигурацию логгеру из словаря с настройками
logging.config.dictConfig(logger_config)

# 3 -шаг
# Получение объекта логгера из файла конфигурации
logger_debug = logging.getLogger('app_logger_debug')
