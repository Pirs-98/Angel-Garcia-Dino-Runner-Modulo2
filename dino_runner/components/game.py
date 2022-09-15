import pygame

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, FONT_STYLE
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager


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
        self.running = False
        self.score = 0
        self.death_count = 0

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
        pygame.display.quit()
        pygame.quit()

    def run(self):
        # Game loop: events - update - draw
        self.reset()
        self.obstacle_manager.reset_obstacles()
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        self.update_score()
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.draw_score()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
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
        text = f'Score: {self.score}'
        pos_center = (1000, 50)
        self.generate_text(text, pos_center)

    def update_score(self):
        self.score += 1

        if self.score % 100 == 0 and self.game_speed < 2000:
            self.game_speed += 2
        

    def handle_events_on_menu(self):
        if self.death_count < 5:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.playing = False
                elif event.type == pygame.KEYDOWN:
                    self.run()
        else:
            pygame.time.delay(3000)
            pygame.quit()
                

    def show_menu(self):
        self.screen.fill((255, 255, 255))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0:
            text = 'Press any key to start ..'
            pos_center = (half_screen_width, half_screen_height + 200)
            self.generate_text(text, pos_center)
        else:
            if self.death_count < 5:
                text =f'Press any key to restart'
                pos_center = (half_screen_width, half_screen_height + 200)
                self.generate_text(text, pos_center)
            if self.death_count > 4:
                text = 'GAME  OVER ...'
                pos_center = (half_screen_width, half_screen_height + 50)
                self.generate_text(text, pos_center)
                text =f'You no longer have lives'
                pos_center = (900, 90)
                self.generate_text(text, pos_center)
            text =f'Your Score: {self.score}'
            pos_center = (half_screen_width, half_screen_height)
            self.generate_text(text, pos_center)
            text =f'Your died {self.death_count} time(s)'
            pos_center = (900, 50)
            self.generate_text(text, pos_center)

        self.screen.blit(ICON, (half_screen_width - 20, half_screen_height - 140))
        pygame.display.update()
        self.handle_events_on_menu()


    def generate_text(self, text, pos_center):
        font = pygame.font.Font(FONT_STYLE, 30)
        text = font.render(text, True, (0, 0, 0))
        text_rec = text.get_rect()
        text_rec.center = pos_center
        self.screen.blit(text, text_rec)

    def reset(self):
        self.score = 0
        self.game_speed = 20