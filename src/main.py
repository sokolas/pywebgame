
import pygame
import asyncio
from api import run_once, serve
from player import get_pos, update_pos


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    serverTask = loop.create_task(serve())

    # настройка pygame
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))

    # установим игрока по центру экрана
    update_pos(screen.get_width() / 2, screen.get_height() / 2)
    player_pos = get_pos()

    clock = pygame.time.Clock()
    dt = 0
    running = True
    while running:
        # проверим события
        # событие pygame.QUIT означает, что нажали на крестик
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("purple")

        # получим текущую позицию игрока
        player_pos = get_pos()
        
        # нарисуем "игрока"
        pygame.draw.circle(screen, "red", player_pos, 40)

        keys = pygame.key.get_pressed()
        
        # обновим позицию, если нажата кнопка
        if keys[pygame.K_w]:
            update_pos(player_pos.x, player_pos.y - 300 * dt)
        if keys[pygame.K_s]:
            update_pos(player_pos.x, player_pos.y + 300 * dt)
        if keys[pygame.K_a]:
            update_pos(player_pos.x - 300 * dt, player_pos.y)
        if keys[pygame.K_d]:
            update_pos(player_pos.x + 300 * dt, player_pos.y)
        
        
        # нарисуем все, что задали, на экране
        pygame.display.flip()

        # проверим fastapi и ответим на запросы, если они были
        run_once(loop)

        dt = clock.tick(60)/1000  # следующий тик, на 60 кадров в сек
    
    loop.close()
    pygame.quit()
