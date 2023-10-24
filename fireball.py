from pygame.sprite import Sprite
from pygame.transform import scale, rotate

from utils import load_sprite


class Fireball(Sprite):
    def __init__(self, speed, cannon):
        Sprite.__init__(self)
        self.speed = speed
        self.cannon = cannon
        self.width = 50
        self.length = 75
        self.image = scale(load_sprite("fb_img"), (self.length, self.width))
        if 1 <= cannon <= 3:
            self.image = rotate(self.image, 180)
            self.position = (100, 200 + self.cannon * 50)
            self.direction = 1
        elif 4 <= cannon <= 6:
            self.position = (500, 200 + (self.cannon - 3) * 50)
            self.direction = 2
        elif 7 <= cannon <= 9:
            self.image = rotate(self.image, -90)
            self.position = (200 + (self.cannon - 6) * 50, 500)
            self.direction = 3
        elif 10 <= cannon <= 12:
            self.image = rotate(self.image, 90)
            self.position = (200 + (self.cannon - 9) * 50, 100)
            self.direction = 4
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def update(self):
        direction_updates = {
            1: (self.speed, 0),
            2: (-self.speed, 0),
            3: (0, -self.speed),
            4: (0, self.speed),
        }
        update = direction_updates.get(self.direction)
        x = self.position[0] + update[0]
        y = self.position[1] + update[1]
        self.position = (x, y)
        self.rect.center = self.position

        if (
            self.position[0] > 550
            or self.position[0] < 50
            or self.position[1] > 550
            or self.position[1] < 50
        ):
            self.kill()
