
from scene import Scene
import pygame
import settings


class GameplayScene(Scene):
    def __init__(self, game):
        self.game = game

    def handle_events(self, events):
        if not self.game.game_state.is_playing():
            return
        for event in events:
            self.game.player.handle_event(event)

            if (
                event.type == pygame.KEYDOWN
                and event.key == settings.shoot_key
            ):
                self.game.projectile_manager.fire(
                    self.game.player, manual=True
                )

    def update(self, dt):
        game = self.game

        if not game.game_state.is_playing():
            return

        game.session.elapsed_time += dt

        game.player.update(
            dt, pygame.key.get_pressed(),
            game.tilemap
        )

        game.checkpoint_manager.update(game.player)

        if game.player.fell_out:
            game.player.lives -= 1

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

        game.projectile_manager.update(dt, game.tilemap)

        if game.boss_room is not None:
            game.boss_room.update(
                dt,
                game.player,
                game.tilemap,
                game.projectile_manager,
                game.camera,
                game.session
            )

        for goal_rect in game.tilemap.goal_rects:
            if game.tilemap.is_goal_loacked(goal_rect):
                continue

            if game.player.rect.colliderect(goal_rect):
                game.change_scene("level_comoplete")
                return

        game.camera.update(game.player, dt)
        
    def draw(self, screen):
        game = self.game

        game.tilemap.draw(screen, game.camera)
        game.checkpoint_manager.draw(screen, game.camera)
        game.coin_manager.draw(screen, game.camera)

        if game.boss_room is not None:
            game.boss_room.draw(screen, game.camera)

        game.projectile_manager.draw(screen, game.camera)
        game.player.draw(screen, game.camera)

        if game.boss_room is not None:
            game.boss_room.draw_ui(screen)