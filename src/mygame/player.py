import pygame
import random

class Player:
    def __init__(self, x, y, name = None):
        if not name:
            self.name = "Player" + str(random.randint(1, 10000))
        else:
            self.name = name
        self.pos = pygame.Vector2(x, y)


    # функции для обновления/получения позиции
    def update_pos(self, x, y):
        self.pos = pygame.Vector2(x, y)

    def get_pos(self):
        return self.pos
    
    def to_dict(self):
        return {"name": self.name, "x": self.pos.x, "y": self.pos.y}
        