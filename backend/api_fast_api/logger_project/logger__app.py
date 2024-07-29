import os
import logging.config

from api_fast_api.config import LOG_DATA_PATH
from api_fast_api.logger_project.logger_config import logger_config


# ======================== Функция создания папки с файлами логгирования
def creat_folder_log_data():
    """Функция создания папки с файлами логгирования"""

    # Проверяем существование папки для логов
    if not os.path.exists(LOG_DATA_PATH):
        try:
            # Создаем папку для логов
            os.makedirs(LOG_DATA_PATH)
            # Создаем файлы для записи логов
            LOG_FILES = ['debug.log', 'warning.log', 'error.log']
            for log_file in LOG_FILES:
                with open(os.path.join(LOG_DATA_PATH, log_file), 'w') as f:
                    f.write('')  # Создаем пустой файл
        except Exception as e:
            print(f'Ошибка при создании папки для логов - {LOG_DATA_PATH}: {e}')


# Так как логгер загружается первым в приложении
# для его корректной работы нужно создать папку Logs для запуска конфигурации
creat_folder_log_data()

# Задаем конфигурацию логгеру из словаря с настройками
logging.config.dictConfig(logger_config)

# Получение объекта логгера из файла конфигурации
logger_debug = logging.getLogger('app_logger_debug')
