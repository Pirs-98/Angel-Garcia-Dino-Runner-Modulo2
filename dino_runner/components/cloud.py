import random
from dino_runner.utils.constants import CLOUD, SCREEN_WIDTH


class Cloud:
    def __init__(self):
        self.image = CLOUD
        self.width = self.image.get_width()
        self.pos_x_cloud = SCREEN_WIDTH + self.width + random.randint(0, 300)
        self.pos_y_cloud = random.randint(50, 200)

    def update(self, cloud_speed):
        self.pos_x_cloud -= cloud_speed
        if self.pos_x_cloud < -self.width:
            self.pos_x_cloud = SCREEN_WIDTH + self.width + random.randint(0, 300)
            self.pos_y_cloud = random.randint(50, 200)

    def draw(self, screen):
        screen.blit(self.image, (self.pos_x_cloud, self.pos_y_cloud))

