import random
import pygame

from dino_runner.utils.constants import BIRD, LARGE_CACTUS, SMALL_CACTUS
from dino_runner.components.obstacles.small_cactus import SmallCactus
from dino_runner.components.obstacles.large_cactus import LargeCactus
from dino_runner.components.obstacles.bird import Bird

class ObstacleManager:
    def __init__(self):
        self.obstacles = [ ]

    def update(self, game):
        if len(self.obstacles) == 0:
            if random.randint(0, 2) == 0:
                small_cactus = SmallCactus(SMALL_CACTUS)
                self.obstacles.append(small_cactus)
            elif random.randint(0, 2) == 1:
                large_cactus = LargeCactus(LARGE_CACTUS)
                self.obstacles.append(large_cactus)
            elif random.randint(0, 2) == 2:
                bird = Bird(BIRD)
                self.obstacles.append(bird) 

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(1000)
                game.playing = False
                break

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)
        
