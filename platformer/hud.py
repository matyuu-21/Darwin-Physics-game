import pygame


class HUD:
    def __init__(self):
        self.font = pygame.font.Font(None, 28)
        self.debug_font = pygame.font.Font(None, 22)

    def draw_text(self, screen, text, x, y, color=(255, 255, 255)):
        image = self.font.render(text, True, color)
        screen.blit(image, (x, y))

    def draw_gameplay(self, screen, game):
        self.draw_text(
            screen,
            f"{game.player.planet_name} | "
            f"{game.player.gravity_scale:.1f}x GRAVITY",
            15, 15
        )

        self.draw_text(
            screen,
            f"Lives: {game.player.lives}",
            15, 50,
            (255, 100, 100)
        )

        self.draw_text(
            screen,
            f"Score: {game.session.score}",
            game.screen.get_width() - 180, 15
        )

        self.draw_text(
            screen,
            f"Coins: {game.session.coins}",
            game.screen.get_width() - 180, 50,
            (255, 215, 0)
        )

        controls = (
            "Move: A/D or Arrows | Jump: Space/W/Up | "
            "Gravity: 1/2/3 | R: Restart | F3: Debug | Esc: Pause"
        )

        control_image = self.debug_font.render(
            controls, True, (255, 255, 255)
        )

        screen.blit(
            control_image,
            (15, screen.get_height() - 30)
        )

    def draw_debug(self, screen, game):
        debug_lines = [
            f"FPS: {game.clock.get_fps():.1f}",
            f"Position: X {game.player.pos.x:.1f} Y {game.player.pos.y:.1f}",
            f"Velocity: X {game.player.vel.x:.1f} Y {game.player.vel.y:.1f}",
            f"On ground: {game.player.on_ground}",
            f"Coyote timer: {game.player.coyote_timer:.3f}",
            f"Jump buffer: {game.player.jump_buffer_timer:.3f}",
            f"Planet: {game.player.planet_name}"
        ]

        background = pygame.Surface((380, 190))
        background.set_alpha(180)
        background.fill((20, 20, 20))

        screen.blit(background, (10, 100))

        for index, line in enumerate(debug_lines):
            image = self.debug_font.render(
                line, True, (255, 255, 255)
            )

            screen.blit(image, (20, 110 + index * 24))