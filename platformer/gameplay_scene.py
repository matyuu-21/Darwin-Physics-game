from scene import Scene
import pygame, settings

class GameplayScene(Scene):
    def __init__(self, game):
        self.game = game

    def handle_events(self, events):
        if not self.game.game_state.is_playing():
            return
        for event in events:
            self.game.player.handle_event(event)

    def update(self, dt):
        game = self.game

        if not game.game_state.is_playing():
            return

        game.player.update(
            dt,
            pygame.key.get_pressed(),
            game.tilemap
        )

        if game.player.fell_out:
            game.player.lives -= 1

            game.player.respawn(game.tilemap.spawn_point)
            game.player.fell_out = False
            game.player.invincible_timer = settings.invincible_time

        for hazard_rect in game.tilemap.hazard_rects:
            if game.player.rect.colliderect(hazard_rect):
                game.player.take_hit(hazard_rect.centerx)

        if game.player.lives <= 0:
            game.change_scene("game_over")
            return

        game.coin_manager.update(dt)

        collected = game.coin_manager.collect(game.player)

        if collected > 0:
            for _ in range(collected):
                game.session.add_coin()

        game.camera.update(game.player, dt)
        
    def draw(self, screen):
        game = self.game

        game.tilemap.draw(screen, game.camera)
        game.coin_manager.draw(screen, game.camera)
        game.player.draw(screen, game.camera)