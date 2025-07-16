# =========== часть про fastapi 
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
import uvicorn
import json

# менеджер соединений
class ConnectionManager:
    """класс, описывающий события от вебсокетов"""
    def __init__(self):
        """список активных соединений"""
        self.active_connections = []
    
    async def connect(self, websocket: WebSocket):
        """событие - подключился новый клиент"""
        await websocket.accept()
        # добавим соединение в список
        self.active_connections.append(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """отправить текстовое сообщение одному из клиентов"""
        await websocket.send_text(message)
    
    async def send_message_all(self, message):
        """отправить текстовое сообщение всем клиентам"""
        for socket in self.active_connections:
            await socket.send_text(message)

    def disconnect(self, websocket: WebSocket):
        """событие - клиент отключился"""
        self.active_connections.remove(websocket)

# весь веб в одном классе
class ServerApi:

    def __init__(self, game, event_loop):
        # event loop для обработки фастапи
        self.loop = event_loop

        # переменная, хранит все fastapi-приложение
        self.app = FastAPI()

        # self.router = ApiRouter()
        self.manager = ConnectionManager()
        
        # наша игра
        self.game = game

        # привяжем все роуты
        self.setup_routes()
        
        # self.router.add_api_route("/", self.get_all_players, methods=["GET"])
        # self.router.add_api_websocket_route("/ws", self.websocket_handler, methods=["GET"])

        # установим их в фастапи приложение
        # self.app.include_router(self.router)

    # установка всех эндпоинтов
    def setup_routes(self):
        # мы объявляем функции внутри метода, чтобы можно было использовать self из его параметров,
        # но при этом не передавать его явно в функции.
        # иначе фастапи будет ругаться, что не может взять self из запроса
        @self.app.get("/")
        async def get_all_players():
            return self.game.get_all_players()

        @self.app.websocket("/ws")
        async def websocket_handler(websocket: WebSocket):
            await self.manager.connect(websocket)
            # это выполняется для каждого нового соединения и работает, пока оно не отсоединится
            try:
                while True:
                    message = await websocket.receive_text()
                    # если от одного из игроков пришло сообщение, значит, он сдвинулся, и надо сообщить об этом игре
                    data = json.loads(message)
                    print(data)
                    if (data["event_type"] == "player_moved"):
                        self.game.move_player(data["data"])

                    # await self.manager.send_personal_message(f"Received:{data}", websocket)
            except WebSocketDisconnect:
                self.manager.disconnect(websocket)
    
    
    # Специальная обертка над сервером, которую надо запускать в цикле внутри игры
    # Если серверу есть что обработать (пришел запрос), он это выполнит
    # Если никаких новых запросов нет - продолжит дальше
    # Обертка нужна, потому что если мы запустим сервер через uvicorn.run, он заблокирует нам цикл, пока не выйдем
    def run_once(self):
        self.loop.call_soon(self.loop.stop)
        self.loop.run_forever()
        
    # запуск сервера в фоновом режиме
    async def serve(self):
        config = uvicorn.Config(app=self.app, port=5000, log_level="info")
        server = uvicorn.Server(config)
        await server.serve()

    def create_task(self):
        return self.loop.create_task(self.serve())

    def close(self):
        self.loop.close()

    def notify(self, data):
        # игра работает на обычных функциях, а веб - на асинхронных,
        # поэтому нам нужна такая "связка" между ними через create_task
        self.loop.create_task(self.manager.send_message_all(json.dumps(data)))
