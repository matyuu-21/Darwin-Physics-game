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

        self.black = (25, 30, 40)
        self.white = (255, 255, 255)
        self.orange = (255, 145, 50)
        self.dark_orange = (220, 105, 25)
        self.gray = (110, 115, 125)

        self.heart_size = 28
        self.heart_start_x = 45
        self.heart_y = 475

        self.heart_full = pygame.image.load(asset_path("assets/heart_red.png")).convert_alpha()
        self.heart_empty = pygame.image.load(asset_path("assets/heart_grey.png")).convert_alpha()

        self.heart_full = pygame.transform.scale(self.heart_full, (self.heart_size, self.heart_size))
        self.heart_empty = pygame.transform.scale(self.heart_empty, (self.heart_size, self.heart_size))

        self.score_x = self.screen_width - 45
        self.score_y = 475
        self.best_y = 515

        self.play_button = pygame.Rect(490, 390, 300, 70)
        self.restart_button = pygame.Rect(490, 420, 300, 70)

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

    def draw_hud(self, score, best_score, lives):
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