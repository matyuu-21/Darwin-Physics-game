import pygame, settings

class GameUI:
    def __init__(self):
        self.font = pygame.font.Font(None, 32)
        self.large_font = pygame.font.Font(None, 64)

    def draw(self, screen, player, score, coins):
        planet_text = self.font.render(
            f"Planet: {player.planet_name}",
            True,
            (255, 255, 255)
        )
        screen.blit(planet_text, (20, 20))

        lives_text = self.font.render(
            f"Lives: {player.lives}",
            True, 
            (255, 100, 100)
        )
        screen.blit(lives_text, (20, 55))

        score_text = self.font.render(
            f"Score: {score}",
            True, (255, 255, 255)
        )
        screen.blit(score_text, (screen.get_width() - 180, 20))

        coin_text = self.font.render(
            f"Coins: {coins}",
            True, (255, 215, 0)
        )
        screen.blit(coin_text, (screen.get_width() - 180, 55))

        coin_text = self.font.render(
            f"Coins: {coins}",
            True, (255, 215, 0)
        )
        screen.blit(coin_text, (screen.get_width() -  180, 55))

    def draw_game_over(self, screen):
        title = self.large_font.render(
            "Game Over",
            True, (255, 80, 80)
        )
        restart = self.font.render(
            "Press R to restart",
            True, (255, 255, 255)
        )

        screen.blit(
            title,
            title.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 30))
        )
        screen.blit(
            restart,
            restart.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 30))
        )