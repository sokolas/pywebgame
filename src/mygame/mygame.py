# состояние и логика игры
class MyGame:
    players = []
    notifier = None # это будет или сервер, или клиент, в зависимости от того, как запущено приложение

    def add_player(self, player):
        self.players.append(player)

    def get_all_players(self):
        return list(map(lambda player: player.to_dict(), self.players))

    # изначально игра не знает, на сервере она запущена или на клиенте,
    # поэтому мы установим "нотификатор" позже через этот метод
    def set_notifier(self, notifier):
        self.notifier = notifier

    # отправить всем игрокам уведомление, что что-то изменилось
    def notify(self, event_type, data):
        if self.notifier:
            self.notifier.notify({"event_type": event_type, "data": data})
