from scene import Scene
import pygame

class GameOverScene(Scene):
    def __init__(self, game):
            self.game = game
    
    def handle_events(self, events):
            for event in events:
                   if event.type == pygame.KEYDOWN:
                          if event.key == pygame.K_r:
                                 self.game.restart_level()
                                 self.game.change_scene("gameplay")
    
    def update(self, dt):
            pass
    
    def draw(self, screen):
        self.game.gameplay_scene.draw(screen)

        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        self.game.ui.draw_game_over(screen)