from mygame.player import Player

# состояние и логика игры
class MyGame:
    players = []
    
    notifier = None # это будет или сервер, или клиент, в зависимости от того, как запущено приложение

    def __init__(self, is_server):
        self.is_server = is_server

    def add_player(self, player):
        self.players.append(player)

    def get_all_players(self):
        return list(map(lambda player: player.to_dict(), self.players))

    # сообщение о том, что один из игроков сдвинулся
    def move_player(self, data):
        name = data["name"]
        x = float(data["x"])
        y = float(data["y"])

        # проверка на то, что это не свой же собственный игрок - не даем другим клиентам управлять им
        if name == self.players[0].name:
            return

        # пройдем по всем известным игрокам и если имя совпало - обновим его позицию
        player_found = False
        for player in self.players:
            if player.name == name:
                player.update_pos(x, y)
                player_found = True
        # если такого игрока не найдено - добавим его
        if not player_found:
            print(f"adding player {name}")
            self.players.append(Player(x, y, name))

        # если мы - сервер, то отправим всем игрокам сообщение о том, что один из них сдвинулся
        if self.is_server:
            self.notify("player_moved", data)

    # изначально игра не знает, на сервере она запущена или на клиенте,
    # поэтому мы установим "нотификатор" позже через этот метод
    def set_notifier(self, notifier):
        self.notifier = notifier

    # отправить всем игрокам уведомление, что что-то изменилось
    def notify(self, event_type, data):
        if self.notifier:
            self.notifier.notify({"event_type": event_type, "data": data})
