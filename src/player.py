import pygame

# позиция игрока
pos = pygame.Vector2(0, 0)

# функции для обновления/получения позиции
def update_pos(x, y):
    global pos
    pos = pygame.Vector2(x, y)

def get_pos():
    global pos
    return pos