import pygame.key
from pygame.sprite import Sprite
from pygame.transform import scale

from utils import load_sprite


class Wizard(Sprite):
    def __init__(self, position):
        Sprite.__init__(self)
        self.position = position
        self.image = scale(load_sprite("wizard_sprite"), (50, 50))
        self.width = 30
        self.height = 30
        self.speed = 5
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = position

    def move(self, action):
        x, y = self.position[0], self.position[1]
        if action == 1 and y > 250:
            y -= 5
        elif action == 2:
            if x < 350:
                x += 5
            if y > 250:
                y -= 5
        elif action == 3 and x < 350:
            x += 5
        elif action == 4:
            if x < 350:
                x += 5
            if y < 350:
                y += 5
        elif action == 5 and y < 350:
            y += 5
        elif action == 6:
            if x > 250:
                x -= 5
            if y < 350:
                y += 5
        elif action == 7 and x > 250:
            x -= 5
        elif action == 8:
            if x > 250:
                x -= 5
            if y > 250:
                y -= 5

        self.position = (x, y)
        self.rect.center = self.position
