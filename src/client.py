import websockets
import json
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError

class ClientApi:

    def __init__(self, uri, game, event_loop):
        self.uri = uri
        self.game = game
        self.loop = event_loop


    def run_once(self):
        self.loop.call_soon(self.loop.stop)
        self.loop.run_forever()

    def create_task(self):
        return self.loop.create_task(self.connect_and_run())

    # loop.create_task(client.connect_and_run())
    async def connect_and_run(self):
        self.ws = await websockets.connect(self.uri)
        try:
            while True:
                response = await self.ws.recv()
                print(response)
                # print(f"Received: {response}")
                # если от сервера пришло сообщение, что игрок сдвинулся, то надо сообщить об этом нашей игре
                data = json.loads(response)
                if (data["event_type"] == "player_moved"):
                    self.game.move_player(data["data"])
        except ConnectionClosedOK:
            print("Connection closed normally.")
        except ConnectionClosedError as e:
            print(f"Connection closed with error: {e}")
        except Exception as e:
            print(f"Unexpected error while receiving: {e}")


    async def send_message(self, msg):
        if self.ws:
            try:
                await self.ws.send(msg)
            except Exception as e:
                print(f"Unexpected error while sending: {e}")
                # error
                # await self.ws.close()


    def notify(self, data):
        # игра работает на обычных функциях, а веб - на асинхронных,
        # поэтому нам нужна такая "связка" между ними через create_task
        self.loop.create_task(self.send_message(json.dumps(data)))