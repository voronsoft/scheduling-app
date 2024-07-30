# Используем официальный образ Python версии 3.12
FROM python:3.12

# Устанавливаем рабочую директорию в контейнере
WORKDIR /scheduling-backend

# Копируем файлы проекта в контейнер
COPY . .

# Устанавливаем зависимости из requirements.txt
RUN pip install -r requirements.txt

# Открываем порт для доступа к приложению
EXPOSE 8888

# Запускаем скрипт для запуска приложения
CMD ["python", "run_fapi_docker.py"]
