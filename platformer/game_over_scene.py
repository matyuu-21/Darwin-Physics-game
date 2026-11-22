
from scene import Scene
import pygame


class GameOverScene(Scene):
    def __init__(self, game):
        self.game = game

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:

                    # Retry only the boss fight if Darwin lost
                    # while the boss room was active.
                    if (
                        self.game.boss_room is not None
                        and self.game.boss_room.is_started()
                    ):
                        self.game.retry_boss()

                    else:
                        self.game.restart_level()
                        self.game.change_scene("gameplay")

    def update(self, dt):
        pass

    def draw(self, screen):
        self.game.gameplay_scene.draw(screen)

        overlay = pygame.Surface(
            screen.get_size(),
            pygame.SRCALPHA
        )

        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        self.game.ui.draw_game_over(screen)

        # Show the appropriate retry instruction.
        font = pygame.font.Font(None, 36)

        if (
            self.game.boss_room is not None
            and self.game.boss_room.is_started()
        ):
            message = "R - Retry Boss"
        else:
            message = "R - Restart Level"

        image = font.render(
            message,
            True,
            (255, 255, 255)
        )

        screen.blit(
            image,
            (
                screen.get_width() // 2 - image.get_width() // 2,
                screen.get_height() // 2 + 100
            )
        )
