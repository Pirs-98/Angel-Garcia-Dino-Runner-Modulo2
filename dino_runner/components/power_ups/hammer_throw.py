import random
from dino_runner.components.obstacles.obstacle import Obstacle
from dino_runner.utils.constants import HAMMER, SCREEN_WIDTH, SCREEN_HEIGHT
from pygame.sprite import Sprite


class HammerThrow(Sprite):
    def __init__(self, player):
        self.image = HAMMER
        self.rect = self.image.get_rect()
        self.rect.x = player.dino_rect.x + player.dino_rect.width
        self.rect.y = player.dino_rect.y
        self.width = self.image.get_width()

    def update(self, throw_speed, hammers_throw):
        self.rect.x += throw_speed
        if self.rect.x > SCREEN_WIDTH + self.rect.width:
            hammers_throw.pop()

    def draw(self, screen):
        screen.blit(self.image, self.rect)