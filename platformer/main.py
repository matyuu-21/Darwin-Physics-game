from pathlib import Path

import pygame, settings

from tilemap import Tilemap
from player import Player
from camera import Camera
from coin_manager import CoinManager
from ui import GameUI

from session import Session
from game_state import GameState
from scene_manager import SceneManager

from gameplay_scene import GameplayScene
from menu_scene import MenuScene
from pause_scene import PauseScene
from game_over_scene import GameOverScene
from hud import HUD
from projectile_manager import ProjectileManager
from checkpoint_manager import CheckpointManager
from level_complete_scene import LevelCompleteScene


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(
            (settings.screen_width, settings.screen_height)
        )
        pygame.display.set_caption("DARWIN'S PLATFORMER")

        self.clock = pygame.time.Clock()

        self.running = True
        self.show_debug = False

        self.base_path = Path(__file__).resolve().parent
        self.level_path = self.base_path / "levels" / "test_level.txt"

        self.background_color = (110, 190, 235)
        self.ui = GameUI()
        self.hud = HUD()

        self.session = Session()
        self.game_state = GameState()
        self.scene_manager = SceneManager()

        self.menu_scene = MenuScene(self)
        self.gameplay_scene = GameplayScene(self)
        self.pause_scene = PauseScene(self)
        self.game_over_scene = GameOverScene(self)
        self.level_complete_scene = LevelCompleteScene(self)

        self.scene_manager.add_scene("menu", self.menu_scene)
        self.scene_manager.add_scene("gameplay", self.gameplay_scene)
        self.scene_manager.add_scene("pause", self.pause_scene)
        self.scene_manager.add_scene("game_over", self.game_over_scene)
        self.scene_manager.add_scene("level_complete", self.level_complete_scene)

        self.restart_level()

        self.change_scene("menu")
        self.game_state.change_state("menu")

    def restart_level(self):
        self.tilemap = Tilemap()
        self.tilemap.load(self.level_path)

        self.player = Player(self.tilemap.spawn_point)
        self.coin_manager = CoinManager(self.tilemap)
        self.checkpoint_manager = CheckpointManager(self.tilemap)
        self.projectile_manager = ProjectileManager()

        self.camera = Camera(
            self.tilemap.width_px,
            self.tilemap.height_px
        )

        self.session.score = 0
        self.session.coins = 0
        self.session.double_score_timer = 0
        self.session.elapsed_time = 0

        self.game_state.change_state("playing")

    def change_scene(self, scene_name):
        self.scene_manager.change_scene(scene_name)

        if scene_name == "gameplay":
            self.game_state.change_state("playing")
        elif scene_name == "menu":
            self.game_state.change_state("menu")
        elif scene_name == "pause":
            self.game_state.change_state("paused")
        elif scene_name == "game_over":
            self.game_state.change_state("game_over")
        elif scene_name == "level_complete":
            self.game_state.change_state("level_complete")

    def handle_events(self):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    if self.game_state.is_playing():
                        self.change_scene("pause")

                    elif self.game_state.is_paused():
                        self.change_scene("gameplay")

                    else:
                        self.running = False

                elif event.key == pygame.K_F3:
                    self.show_debug = not self.show_debug

                elif event.key == pygame.K_r:
                    if self.game_state.is_playing():
                        self.player.respawn(self.tilemap.spawn_point)
                        self.player.fell_out = False

        # ESC is handled above, so don't send it to the active scene.
        scene_events = [
            event for event in events
            if not (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE
            )
        ]

        self.scene_manager.handle_events(scene_events)

    def update(self, dt):
        dt = min(dt, 1 / 30)

        self.session.update(dt)
        self.scene_manager.update(dt)

    def draw_text(self, text, x, y, color=(255, 255, 255)):
        image = self.font.render(text, True, color)
        self.screen.blit(image, (x, y))

    def draw_debug(self):
        debug_lines = [
            f"FPS: {self.clock.get_fps():.1f}",
            f"Position: X {self.player.pos.x:.1f} Y {self.player.pos.y:.1f}",
            f"Velocity: X {self.player.vel.x:.1f} Y {self.player.vel.y:.1f}",
            f"On ground: {self.player.on_ground}",
            f"Coyote timer: {self.player.coyote_timer:.3f}",
            f"Jump buffer: {self.player.jump_buffer_timer:.3f}",
            f"Planet: {self.player.planet_name}"
        ]

        background = pygame.Surface((380, 190))
        background.set_alpha(180)
        background.fill((20, 20, 20))

        self.screen.blit(background, (10, 100))

        for index, line in enumerate(debug_lines):
            image = self.debug_font.render(
                line, True, (255, 255, 255)
            )
            self.screen.blit(
                image, (20, 110 + index * 24)
            )

    def draw(self):
        self.screen.fill(self.background_color)

        self.scene_manager.draw(self.screen)

        if self.game_state.is_playing():

            self.hud.draw_gameplay(self.screen,self)

            if self.show_debug:
                self.hud.draw_debug(self.screen,self)

        pygame.display.flip()

    def run(self):

        while self.running:
            dt = self.clock.tick(settings.fps) / 1000

            self.handle_events()
            self.update(dt)
            self.draw()



if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()