from random import sample

import pygame

from fireball import Fireball
from utils import load_sprite, draw_text, save_score, load_score, place_cannons
from wizard import Wizard


class WizGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Ember Lord")

        self.screen = pygame.display.set_mode((600, 600))

        self.game_over = False

        self.FPS = 60

        self.background = pygame.transform.scale(
            load_sprite("lava_ground", False), (600, 600)
        )
        self.floor = pygame.transform.scale(
            load_sprite("metal_platform", False), (150, 150)
        )

        self.wiz_position = (300, 300)
        self.wizard = Wizard(self.wiz_position)
        self.wiz_health = 3

        self.action = 0

        self.fb_group = pygame.sprite.Group()

        self.fb_speed = 3
        self.fb_num = 1
        self.difficulty_counter = 0
        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()
        self.timer_start_time = self.start_time
        self.highscore = load_score()
        self._fire_fireball()

    def main_loop(self):
        while self.game_over == False:
            self._update_time()
            self._handle_input()
            self.wizard.move(self.action)
            self._game_logic()
            self._draw()

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and keys[pygame.K_d]:
            self.action = 2
        elif keys[pygame.K_s] and keys[pygame.K_d]:
            self.action = 4
        elif keys[pygame.K_s] and keys[pygame.K_a]:
            self.action = 6
        elif keys[pygame.K_w] and keys[pygame.K_a]:
            self.action = 8
        elif keys[pygame.K_w]:
            self.action = 1
        elif keys[pygame.K_d]:
            self.action = 3
        elif keys[pygame.K_s]:
            self.action = 5
        elif keys[pygame.K_a]:
            self.action = 7
        else:
            self.action = 0

    def _game_logic(self):
        self.wiz_position = (self.wizard.position[0], self.wizard.position[1])

        for fireball in self.fb_group:
            fireball.update()

        if self.elapsed_time >= 3000:
            self._fire_fireball()
            self._update_difficulty()
            self.start_time = self.current_time

        self._handle_collisions()

        if self.wiz_health <= 0:
            if self.timer_time > self.highscore:
                self.highscore = round(self.timer_time, 2)
                save_score(self.highscore)
            self.game_over = True

    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.floor, (225, 225))
        self.screen.blit(
            self.wizard.image, (self.wizard.rect[0] - 10, self.wizard.rect[1] - 10)
        )
        self.fb_group.draw(self.screen)

        cannons = place_cannons()
        for i in range(12):
            self.screen.blit(cannons[i][0], cannons[i][1])

        lives_text = draw_text(f"Lives: {self.wiz_health}")
        self.screen.blit(lives_text, [50, 25])
        time_text = draw_text(f"Time: {self.timer_time}")
        self.screen.blit(time_text, [425, 25])
        highscore_text = draw_text(f"Highscore: {self.highscore}")
        self.screen.blit(highscore_text, [170, 25])

        pygame.display.flip()
        self.clock.tick(self.FPS)

    def _fire_fireball(self):
        cannons = sample(range(1, 13), self.fb_num)
        for i in range(self.fb_num):
            fireball = Fireball(self.fb_speed, cannons[i])
            self.fb_group.add(fireball)

    def _update_time(self):
        self.current_time = pygame.time.get_ticks()
        self.elapsed_time = self.current_time - self.start_time
        self.timer_time = round((self.current_time - self.timer_start_time) / 1000, 2)

    def _handle_collisions(self):
        collided_fireball = pygame.sprite.spritecollideany(self.wizard, self.fb_group)
        if collided_fireball:
            collided_fireball.kill()
            self.wiz_health -= 1

    def _update_difficulty(self):
        self.difficulty_counter += 1
        counter = self.difficulty_counter
        if counter in (1, 3, 7, 9, 14, 19):
            self.fb_speed += 0.5
        elif counter == 4:
            self.fb_num += 1
