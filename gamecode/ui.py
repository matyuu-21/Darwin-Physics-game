import pygame
from asset_path import asset_path

class GameUI:
    def __init__(self, screen):
        self.screen = screen

        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        self.game_font = pygame.font.Font(None, 40)
        self.title_font = pygame.font.Font(None, 90)
        self.small_font = pygame.font.Font(None, 30)
        self.stage_font = pygame.font.Font(None, 45)

        self.black = (25, 30, 40)
        self.white = (255, 255, 255)
        self.orange = (255, 145, 50)
        self.dark_orange = (220, 105, 25)
        self.gray = (110, 115, 125)

        self.heart_size = 28
        self.heart_start_x = 45
        self.heart_y = 530

        self.heart_full = pygame.image.load(asset_path("assets/heart_red.png")).convert_alpha()
        self.heart_empty = pygame.image.load(asset_path("assets/heart_grey.png")).convert_alpha()

        self.heart_full = pygame.transform.scale(self.heart_full, (self.heart_size, self.heart_size))
        self.heart_empty = pygame.transform.scale(self.heart_empty, (self.heart_size, self.heart_size))

        self.score_x = self.screen_width - 45
        self.score_y = 520
        self.best_y = 550

        self.play_button = pygame.Rect(490, 390, 300, 70)
        self.restart_button = pygame.Rect(490, 420, 300, 70)

        self.world_buttons = [
            pygame.Rect(105, 300, 320, 230),
            pygame.Rect(480, 300, 320, 230),
            pygame.Rect(855, 300, 320, 230)
        ]
        self.stage_buttons = [
            pygame.Rect(105, 315, 320, 190),
            pygame.Rect(480, 315, 320, 190),
            pygame.Rect(855, 315, 320, 190)
        ]
        self.back_button = pygame.Rect(45, 45, 150, 55)

    def draw_text(self, text, font, color, x, y):
        image = font.render(text, True, color)
        rect = image.get_rect(center=(x, y))
        self.screen.blit(image, rect)

    def draw_button(self, rect, text):
        mouse_pos = pygame.mouse.get_pos()

        if rect.collidepoint(mouse_pos):
            color = self.dark_orange
        else: 
            color = self.orange

        pygame.draw.rect(
            self.screen, color, rect, border_radius=14
        )

        self.draw_text(
            text, self.game_font, self.white,
            rect.centerx, rect.centery
        )

    def draw_heart(self, x, y, size, color):
        radius = size // 4

        pygame.draw.circle(
            self.screen, color,
            (x + radius, y + radius), radius
        )

        pygame.draw.circle(
            self.screen, color, 
            (x + size - radius, y + radius), radius
        )

        points = [
            (x, y + radius),
            (x + size, y + radius),
            (x + size // 2, y + size)
        ]

        pygame.draw.polygon(self.screen, color, points)

    def draw_health(self, lives):
        for i in range(3):
            if i < lives:
                heart_image = self.heart_full
            else: 
                heart_image = self.heart_empty

            x = self.heart_start_x + i * (self.heart_size + 10)

            self.screen.blit(
                heart_image, (x, self.heart_y)
            )

    def draw_hud(self, score, best_score, lives, gravity_text=""):
        self.draw_health(lives)

        score_image = self.game_font.render(
            f"SCORE: {int(score):05d}", True, self.black
        )
        score_rect = score_image.get_rect(
            midright=(self.score_x, self.score_y)
        )
        self.screen.blit(score_image, score_rect)

        best_image = self.small_font.render(
            f"BEST: {best_score:05d}", True, self.gray
        )
        best_rect = best_image.get_rect(
            midright=(self.score_x, self.best_y)
        )
        self.screen.blit(best_image, best_rect)

        if gravity_text:
            grav_image = self.small_font.render(gravity_text, True, self.gray)
            grav_rect = grav_image.get_rect(midright=(self.score_x, self.best_y + 28))
            self.screen.blit(grav_image, grav_rect)

    def draw_world_select(self, worlds):
        self.screen.fill((255, 235, 245))
        self.draw_text("DARWIN'S JOURNEY", self.title_font, self.black,
                       self.screen_width // 2, 110)
        self.draw_text("SELECT YOUR WORLD", self.game_font, self.gray,
                       self.screen_width // 2, 205)

        for index, world in enumerate(worlds):
            rect = self.world_buttons[index]
            available = world["available"]
            color = self.orange if available else (155, 160, 170)
            pygame.draw.rect(self.screen, color, rect, border_radius = 18)
            pygame.draw.rect(self.screen, self.white, rect, 4, border_radius = 18)
            self.draw_text(world["name"], self.title_font, self. white,
                           rect.centerx, rect.centery)
        self.draw_text("Choose a world", self.small_font, self.gray, self.screen_width // 2, 610)

    def draw_stage_select(self, world, stages):
        self.screen.fill((255, 235, 245))
        self.draw_button(self.back_button, "BACK")
        self.draw_text(world["name"], self.title_font, self.black,
                       self.screen_width // 2, 125)
        self.draw_text("SELECT A STAGE", self.game_font, self.gray,
                       self.screen_width // 2, 205)

        for button_index, (stage_indx, stage) in enumerate(stages):
            rect = self.stage_buttons[button_index]
            available = stage.get("unlocked", True)
            color = self.orange if available else (155, 160, 170)
            pygame.draw.rect(self.screen, color, rect, border_radius = 18)
            pygame.draw.rect(self.screen, self.white, rect, 4, border_radius = 18)
            self.draw_text(str(button_index + 1), self.title_font, self. white,
                           rect.centerx, rect.centery - 35)
            self.draw_text(stage["name"], self.stage_font, self. white,
                           rect.centerx, rect.centery + 30)
            status = "BOSS STAGE" if available else "LOCKED"
            self.draw_text(status, self.small_font, self.white, rect.centerx, rect.bottom - 30)

        if world["name"] == "EARTH":
            hint = "Each Classroom ends with a boss fight"
        else:
            hint = "Planet stages and bosses soon"
        self.draw_text(hint, self.small_font, self.gray, self.screen_width // 2, 590)
    
    def draw_menu(self):
        overlay = pygame.Surface(
        (self.screen_width, self.screen_height), 
        pygame.SRCALPHA
        )
        overlay.fill((255, 255, 255, 190))
        self.screen.blit(overlay, (0, 0))

        self.draw_text(
            "darwin laptop test", 
            self.title_font,
            self.black, 
            self.screen_width // 2, 
            210 
        )

        self.draw_text(
            "a running game", 
            self.small_font,
            self.gray, 
            self.screen_width // 2, 
            275
        )

        self.draw_button(self.play_button, "PLAY")

        self.draw_text(
            "space/up = jump",
            self.small_font,
            self.gray,
            self.screen_width // 2,
            510
        )

        self.draw_text(
            "hold down to duck",
            self.small_font,
            self.gray,
            self.screen_width // 2,
            545
        )

    def draw_game_over(self, score, best_score):
        overlay = pygame.Surface(
            (self.screen_width, self.screen_height),
            pygame.SRCALPHA
        )
        overlay.fill((255, 255, 255, 200))
        self.screen.blit(overlay, (0,0))

        self.draw_text(
            "GAME OVER", self.title_font, self.black, self.screen_width // 2, 220
        )

        self.draw_text(
            f"SCORE {int(score)}",
            self.game_font, self.black, self.screen_width // 2, 300
            )

        self.draw_text(
            f"BEST: {best_score}",
            self.game_font, self.gray, self.screen_width // 2, 345
            )

        self.draw_button(self.restart_button, "PLAY AGAIN")

        self.draw_text(
            "press space/enter to restart",
            self.small_font, self.gray, self.screen_width // 2, 530
            )