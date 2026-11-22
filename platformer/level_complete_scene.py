
from scene import Scene
import pygame


class LevelCompleteScene(Scene):
    def __init__(self, game):
        self.game = game

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.game.restart_level()
                    self.game.change_scene("gameplay")

                elif event.key == pygame.K_m:
                    self.game.change_scene("menu")

    def update(self, dt):
        pass

    def draw(self, screen):
        game = self.game

        screen.fill((25, 45, 65))

        title_font = pygame.font.Font(None, 80)
        info_font = pygame.font.Font(None, 42)
        small_font = pygame.font.Font(None, 30)

        title = title_font.render("LEVEL COMPLETE!", True, (80, 255, 140))
        score = info_font.render(
            f"Final Score: {game.session.score}",
            True,
            (255, 255, 255)
        )
        coins = info_font.render(
            f"Coins Collected: {game.session.coins}",
            True,
            (255, 220, 50)
        )

        minutes = int(game.session.elapsed_time // 60)
        seconds = int(game.session.elapsed_time % 60)

        time_text = info_font.render(
            f"Completion Time: {minutes:02}:{seconds:02}",
            True,
            (255, 255, 255)
        )

        restart = small_font.render("R - Play Again", True, (200, 200, 200))
        menu = small_font.render("M - Main Menu", True, (200, 200, 200))

        center_x = screen.get_width() // 2

        screen.blit(title, title.get_rect(center=(center_x, 200)))
        screen.blit(score, score.get_rect(center=(center_x, 330)))
        screen.blit(coins, coins.get_rect(center=(center_x, 390)))
        screen.blit(time_text, time_text.get_rect(center=(center_x, 450)))
        screen.blit(restart, restart.get_rect(center=(center_x, 560)))
        screen.blit(menu, menu.get_rect(center=(center_x, 600)))
