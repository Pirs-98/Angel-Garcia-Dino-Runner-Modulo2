import pygame, random
from dino_runner.components.power_ups.power_up_manager import PowerUpManager

from dino_runner.utils.constants import BIRD, DEFAULT_TYPE, LARGE_CACTUS, SHIELD_TYPE, SMALL_CACTUS
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

        hammer_thr = None
        if len(game.hammer_throw_manager.hammers_throw) > 0:
            hammer_thr = game.hammer_throw_manager.hammers_throw[0]
            hammer_thr.update(game.throw_speed, self)
        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if hammer_thr and hammer_thr.rect.colliderect(obstacle.rect):
                self.obstacles.remove(obstacle)
                game.hammer_throw_manager.hammers_throw.remove(hammer_thr)
                game.player.has_power_up = False
                game.player.type = DEFAULT_TYPE
            if game.player.dino_rect.colliderect(obstacle.rect):
                if game.player.type != SHIELD_TYPE:
                    pygame.time.delay(1000)
                    game.death_count += 1
                    game.playing = False
                    game.player.has_power_up = False
                    game.player.type = DEFAULT_TYPE
                    break
                else:
                    self.obstacles.remove(obstacle)


    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def reset_obstacles(self):
        self.obstacles = []
