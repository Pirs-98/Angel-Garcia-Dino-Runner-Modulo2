import pygame, random
from dino_runner.components.power_ups.power_up_manager import PowerUpManager

from dino_runner.utils.constants import BIRD, DEFAULT_TYPE, LARGE_CACTUS, SHIELD_TYPE, HAMMER_TYPE, SMALL_CACTUS, SOUND
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
        hammers_throw = game.hammer_throw_manager.hammers_throw
        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if game.player.type != (SHIELD_TYPE):
                    pygame.time.delay(1000)
                    SOUND['DEAD_SOUND'].play()
                    game.death_count += 1
                    game.player.has_shield_power_up = False
                    game.player.has_hammer_power_up = False
                    game.player.type = DEFAULT_TYPE
                    game.playing = False
                    break
                else:
                    self.obstacles.remove(obstacle)
            for hammer_throw in hammers_throw:
                hammer_throw.update(game.throw_speed, hammers_throw)
                if hammer_throw.rect.colliderect(obstacle.rect):
                    self.obstacles.remove(obstacle)
                    hammers_throw.remove(hammer_throw)
                    game.player.has_hammer_power_up = False
                    game.player.type = DEFAULT_TYPE
                


    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def reset_obstacles(self):
        self.obstacles = []
