# =========== часть про fastapi 
from fastapi import FastAPI
import asyncio
import uvicorn

from player import get_pos

# переменная, хранит все fastapi-приложение
app = FastAPI()


# задаем ендпоинты, можно сделать это в отдельных файлах

# получить позицию игрока
@app.get("/")
async def root():
    p = get_pos()
    return {"x": p.x, "y": p.y}

# Специальная обертка над сервером, которую надо запускать в цикле внутри игры
# Если серверу есть что обработать (пришел запрос), он это выполнит
# Если никаких новых запросов нет - продолжит дальше
# Обертка нужна, потому что если мы запустим сервер через uvicorn.run, он заблокирует нам цикл, пока не выйдем
def run_once(loop):
    loop.call_soon(loop.stop)
    loop.run_forever()

# запуск сервера в фоновом режиме
async def serve():
    # api:app - это файл:приложение (фастапи), если оно определено в другом файле, надо указать его имя. Здесь - api потому что оно в api.py
    config = uvicorn.Config("api:app", port=5000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()    
