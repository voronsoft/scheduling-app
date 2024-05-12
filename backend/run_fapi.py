import uvicorn
from api_fast_api.models.models_sql import create_database
from api_fast_api.func.create_project_structure_file import create_project_structure

if __name__ == "__main__":
    # Запускаем построение структуры папок и файлов в проекте
    create_project_structure()
    print("Структура проекта успешно сохранена в файле.")

    # Создаем базу данных перед запуском приложения
    create_database()

    # Запускаем приложение по заданному адресу.
    uvicorn.run("api_fast_api:app", host="127.0.0.10", port=8888)

# TODO Нужно при рефакторинге добавить какие параметры возвращают функции
