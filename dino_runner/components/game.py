import pygame, sys

from dino_runner.components.cloud import Cloud
from dino_runner.components.message import draw_message
from dino_runner.components.power_ups.hammer_throw_manager import HammerThrowManager
from dino_runner.utils.constants import BG, CLOUD, GAME_OVER, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, SOUND, TITLE, FPS, FONT_STYLE, DEFAULT_TYPE
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()
        self.hammer_throw_manager = HammerThrowManager()
        self.cloud = Cloud()
        self.cloud_speed = self.game_speed - 8
        self.running = False
        self.score = 0
        self.best_score = 0
        self.death_count = 0
        self.life_count = 5
        self.throw_speed = self.game_speed + 10

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
        pygame.display.quit()
        pygame.quit()
    
    def reset_game(self):
        self.reset()
        self.obstacle_manager.reset_obstacles()
        self.playing = True
        self.power_up_manager.reset_power_ups()
        self.hammer_throw_manager.reset_hammers_throw()

    def run(self):
        # Game loop: events - update - draw
        self.reset_game()
        SOUND['START_SOUND'].play()
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        self.cloud.update(self.cloud_speed)
        self.update_score()
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.hammer_throw_manager.update(self, user_input)
        self.power_up_manager.update(self)
        self.obstacle_manager.update(self)
        self.update_lifes()

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.cloud.draw(self.screen)
        self.draw_score()
        self.draw_power_up_time()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        self.hammer_throw_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_score(self):
        draw_message(f'Score {self.score}', self.screen, pos_x_center = 1000, pos_y_center = 50)

    def draw_power_up_time(self):
        if self.player.has_hammer_power_up or self.player.has_shield_power_up:
            time_to_show = round((self.player.power_time_up - pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
                draw_message(f'{self.player.type.capitalize()} enable for {time_to_show} seconds', self.screen, font_size = 19, pos_y_center = 100)
            else:
                self.player.has_hammer_power_up = False
                self.player.has_shield_power_up = False
                self.player.type = DEFAULT_TYPE

    def update_score(self):
        self.score += 1
        if self.score % 100 == 0 and self.game_speed < 2000:
            self.game_speed += 1.5
        if self.score > self.best_score:
            self.best_score = self.score

    def update_lifes(self):
        self.life_count = 5 - self.death_count
        
    def handle_events_on_menu(self):
        if self.death_count > 4:
            pygame.time.delay(4000)
            pygame.quit()
            sys.exit()
            pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
            elif event.type == pygame.KEYDOWN:
                self.run()

    def show_menu(self):
        self.screen.fill((255, 255, 255))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2
        self.screen.blit(ICON, (half_screen_width - 40, half_screen_height - 120))

        if self.death_count == 0:
            draw_message('Press any key to start ..', self.screen, pos_y_center = half_screen_height + 100)
            draw_message(f'You start with {self.life_count} lifes', self.screen, pos_y_center = 500)
        else:
            if self.death_count < 5:
                draw_message('Press any key to restart', self.screen, pos_y_center = half_screen_height + 100)
                draw_message(f'You have {self.life_count} lifes', self.screen, font_size = 25, pos_y_center = 500)
            if self.death_count > 4:
                self.screen.blit(GAME_OVER, (355, 150))
                draw_message('You no longer have lives', self.screen, font_size = 25, pos_y_center = 500)
            draw_message(f'Your Score: {self.score}', self.screen, pos_y_center = half_screen_height + 40)
            draw_message(f'High Score: {self.best_score}', self.screen)
            draw_message(f'Death count: {self.death_count}', self.screen, font_size = 25, pos_x_center = 1000, pos_y_center = 30)
            
        pygame.display.update()
        self.handle_events_on_menu()

    def reset(self):
        self.score = 0
        self.game_speed = 20