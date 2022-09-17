import pygame, random

from dino_runner.utils.constants import BIRD, LARGE_CACTUS, SHIELD_TYPE, SMALL_CACTUS
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird

class ObstacleManager:
    def __init__(self):
        self.obstacles = [ ]

    def update(self, game):
        if len(self.obstacles) == 0:
            if random.randint(0, 1) == 0:
                list_of_cactus = SMALL_CACTUS + LARGE_CACTUS
                cactus = Cactus(list_of_cactus)
                self.obstacles.append(cactus)
            else:
                bird = Bird(BIRD)
                self.obstacles.append(bird) 

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if game.player.type != SHIELD_TYPE:
                    pygame.time.delay(1000)
                    game.death_count += 1
                    game.playing = False
                    break
                else:
                    self.obstacles.remove(obstacle)
                            

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def reset_obstacles(self):
        self.obstacles = []
