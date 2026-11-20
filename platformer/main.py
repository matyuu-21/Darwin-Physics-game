from pathlib import Path
from tilemap import Tilemap
from player import Player
from camera import Camera

import pygame, settings

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(
            (settings.screen_width, settings.screen_height)
        )
        pygame.display.set_caption("DARWIN'S PLATFORMER")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 28)
        self.debug_font = pygame.font.Font(None, 22)

        self.running = True
        self.show_debug = False

        self.base_path = Path(__file__).resolve().parent

        self.tilemap = Tilemap()

        level_path = self.base_path / "levels" / "test_level.txt"
        self.tilemap.load(level_path)

        self.player = Player(self.tilemap.spawn_point)

        self.camera = Camera(
            self.tilemap.width_px,
            self.tilemap.height_px
        )

        self.background_color = (110, 190, 235)

    def handle_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    self.running = False

                elif event.key == pygame.K_r: #respawn
                    self.player.respawn(self.tilemap.spawn_point)

                elif event.key == pygame.K_F3: #debug
                    self.show_debug = not self.show_debug

            self.player.handle_event(event)

    def update(self, dt):
        dt = min(dt, 1 / 30)

        keys = pygame.key.get_pressed()

        self.player.update(dt, keys, self.tilemap)

        self.camera.update(self.player, dt)

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

        self.screen.blit(background, (10, 55))

        for index, line in enumerate(debug_lines):
            image = self.debug_font.render(
                line, True, (255, 255, 255)
            )
            self.screen.blit(
                image, (20, 65 + index * 24)
            )

    def draw(self):
        self.screen.fill(self.background_color)
        self.tilemap.draw(self.screen, self.camera)
        self.player.draw(self.screen, self.camera)

        gravity_text = (
            f"{self.player.planet_name} | "
            f"{self.player.gravity_scale:.1f}x GRAVITY"
        )

        self.draw_text(gravity_text, 15, 15)

        controls = (
            "Move: A/D or Arrows | Jump: Space/W/Up | "
            "Gravity: 1/2/3 | Respawn: R | Debug: F3 | Quit: Esc"
        )

        control_image = self.debug_font.render(
            controls, True, (255, 255, 255)
        )

        self.screen.blit(
            control_image, (15, settings.screen_height - 30)
        )

        if self.show_debug:
            self.draw_debug()

        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(settings.fps) / 1000

            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()