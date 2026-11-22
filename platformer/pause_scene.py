from scene import Scene
import pygame

class PauseScene(Scene):
    def __init__(self, game):
        self.game = game

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.change_scene("gameplay")

    def update(self, dt):
        pass

    def draw(self, screen):
        self.game.gameplay_scene.draw(screen)

        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        font = pygame.font.Font(None, 80)
        text = font.render("PAUSED", True, (255, 255, 255))
        rect = text.get_rect(center=screen.get_rect().center)

        screen.blit(text, rect)

        