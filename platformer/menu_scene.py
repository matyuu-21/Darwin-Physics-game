from scene import Scene
import pygame

class MenuScene(Scene):
    def __init__(self, game):
        self.game = game

        self.title_font = pygame.font.Font(None, 100)
        self.button_font = pygame.font.Font(None, 48)

        self.start_button = pygame.Rect(0, 0, 260, 70)
        self.start_button.center = (
            game.screen.get_width() // 2,
            game.screen.get_height() // 2 + 80
        )

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.start_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.start_button.collidepoint(event.pos):
                            self.start_game()

    def start_game(self):
        self.game.restart_level()
        self.game.change_scene("gameplay")

    def update(self, dt):
        pass

    def draw(self, screen):
        title = self.title_font.render(
            "DARWIN JOURNEY", True, (255, 255, 255)
        )

        title_rect = title.get_rect(
            center=(screen.get_width() // 2, screen.get_height() // 2 - 100)
        )
        screen.blit(title, title_rect)

        pygame.draw.rect(
            screen, (40, 120, 70), self.start_button, border_radius=12
        )

        pygame.draw.rect(
            screen, (255, 25, 255), self.start_button,
            width=3, border_radius=12
        )

        button_text = self.button_font.render(
            "START GAME", True, (255, 255, 255)
        )

        button_rect = button_text.get_rect(
            center=self.start_button.center
        )

        screen.blit(button_text, button_rect)