import random

from dino_runner.components.obstacles.obstacle import Obstacle


class Cactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0,5)
        super().__init__(image, self.type)
        self.rect.y = self.y_pos_cactus()

    def y_pos_cactus(self):
        if 0 <= self.type <= 2:
            return 325
        else:
            return 300
