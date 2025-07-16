
import pygame
import asyncio
import random
import sys
from api import ServerApi
from client import ClientApi

from mygame.player import Player
from mygame.mygame import MyGame


if __name__ == "__main__":
    # проверим параметры запуска - клиент мы или сервер
    if len(sys.argv) < 2:
        print("use 'python main.py <server|client>'")
        sys.exit(0)

    is_server = False
    if sys.argv[1] == "server":
        is_server = True
    elif sys.argv[1] == "client":
        is_server = False
    else:
        print("use 'python main.py <server|client>'")
        sys.exit(0)


    # создадим игру
    game = MyGame(is_server)

    # настроим веб-часть и event loop
    loop = asyncio.get_event_loop()
    web_api = ServerApi(game, loop) if is_server else ClientApi("ws://127.0.0.1:5000/ws", game, loop)
    webTask = web_api.create_task()

    # подставим сервер в игру как notifier
    game.set_notifier(web_api)

    # настройка pygame
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    font = pygame.font.Font(pygame.font.get_default_font(), 36)

    # создадим своего игрока, установим игрока по центру экрана и дообавим в список игроков
    my_player = Player(screen.get_width() / 2, screen.get_height() / 2)
    game.add_player(my_player)
    # my_player.update_pos()

    clock = pygame.time.Clock()
    dt = 0
    running = True

    # основной игровой цикл
    while running:
        # проверим события
        # событие pygame.QUIT означает, что нажали на крестик
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if is_server:
            screen.fill("purple")
        else:
            screen.fill("cyan")

        keys = pygame.key.get_pressed()

        # обработаем всех игроков, которые есть в игре
        for player in game.players:
            
            # получим текущую позицию игрока
            player_pos = player.get_pos()
        
            # нарисуем "игрока"
            # pygame.draw.circle(screen, "red", player_pos, 40)
            text_surface = font.render(player.name, True, (0, 0, 0))
            screen.blit(text_surface, dest=player_pos)

            # если игрок, которого мы смотрим - наш, то обновим его позицию, если нажата кнопка
            if player.name == my_player.name:      
                if keys[pygame.K_w]:
                    my_player.update_pos(player_pos.x, player_pos.y - 300 * dt)
                if keys[pygame.K_s]:
                    my_player.update_pos(player_pos.x, player_pos.y + 300 * dt)
                if keys[pygame.K_a]:
                    my_player.update_pos(player_pos.x - 300 * dt, player_pos.y)
                if keys[pygame.K_d]:
                    my_player.update_pos(player_pos.x + 300 * dt, player_pos.y)
                # если игрок сдвинулся, то попросим игру сообщить об этом всем игрокам
                if my_player.pos != player_pos:
                    game.notify("player_moved", my_player.to_dict())
        
        # нарисуем все, что задали, на экране
        pygame.display.flip()

        # проверим fastapi и ответим на запросы, если они были
        web_api.run_once()

        dt = clock.tick(60)/1000  # следующий тик, на 60 кадров в сек
    
    web_api.close()
    pygame.quit()
