import pygame, random
from dino_runner.components.obstacles import obstacle

from dino_runner.components.obstacles.obstacle import Obstacle
from dino_runner.components.power_ups.hammer_throw import HammerThrow
from dino_runner.utils.constants import DEFAULT_TYPE


class HammerThrowManager:
    def __init__(self):
        self.hammers_throw = []

    def update(self, game, user_input):
        if user_input[pygame.K_RIGHT] and len(self.hammers_throw) == 0 and game.player.has_power_up:
            hammer_throw = HammerThrow(game.player)
            self.hammers_throw.append(hammer_throw)
                
    def draw(self, screen):
        for hammer_throw in self.hammers_throw:
            hammer_throw.draw(screen)

    def reset_hammers_throw(self):
        self.hammers_throw = []

