import uvicorn

if __name__ == "__main__":
    # Запускаем приложение.
    uvicorn.run("api_fast_api:app", host="127.0.0.10", port=8888)
