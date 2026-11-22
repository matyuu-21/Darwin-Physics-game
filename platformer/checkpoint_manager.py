
import pygame
import settings


class CheckpointManager:
    def __init__(self, tilemap):
        self.checkpoints = tilemap.checkpoint_rects
        self.active_checkpoint = tilemap.spawn_point
        self.active_index = -1

    def update(self, player):
        for index, checkpoint_rect in enumerate(self.checkpoints):
            if player.rect.colliderect(checkpoint_rect):
                if index != self.active_index:
                    self.active_index = index

                    spawn_x = (
                        checkpoint_rect.centerx
                        - settings.player_width // 2
                    )

                    spawn_y = (
                        checkpoint_rect.bottom
                        - settings.player_height
                    )

                    self.active_checkpoint = (
                        float(spawn_x),
                        float(spawn_y)
                    )

    def respawn_point(self):
        return self.active_checkpoint

    def draw(self, screen, camera):
        for index, checkpoint_rect in enumerate(self.checkpoints):
            screen_rect = camera.apply(checkpoint_rect)

            color = settings.checkpoint_color

            if index == self.active_index:
                color = (0, 255, 100)

            pygame.draw.rect(screen, color, screen_rect)
            pygame.draw.rect(
                screen,
                (30, 30, 30),
                screen_rect,
                3
            )
