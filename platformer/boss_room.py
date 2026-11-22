
import pygame
import settings
from boss import Boss


class BossRoom:
    def __init__(self, boss_id, tilemap):
        self.boss_id = boss_id
        self.tilemap = tilemap

        # Create the boss at the X marker in the level.
        self.boss = Boss(
            boss_id,
            tilemap.boss_spawn,
            tilemap
        )

        # Room states: waiting, intro, fight, cleared
        self.state = "waiting"
        self.state_timer = 0

        # Message shown after defeating the boss.
        self.popup_timer = 0
        self.popup_text = ""

    def update(
        self,
        dt,
        player,
        tilemap,
        projectile_manager,
        camera,
        session
    ):
        self.popup_timer = max(0, self.popup_timer - dt)

        # Keep the dormant boss facing the player.
        if self.state == "waiting":
            self.boss.update(dt, player, tilemap)

            trigger_x = (
                tilemap.boss_room_left
                + settings.boss_trigger_tiles * settings.tile
            )

            if player.rect.centerx > trigger_x:
                self.state = "intro"
                self.state_timer = settings.boss_intro_time

                # Close the entrance behind the player.
                tilemap.close_gate()

                # Lock the camera around the boss room.
                room_center = (
                    tilemap.boss_room_left
                    + settings.boss_room_columns * settings.tile / 2
                )

                camera_target = room_center - settings.screen_width / 2
                camera.lock_to(camera_target)

                # Remove projectiles fired before entering the room.
                projectile_manager.clear()

            return

        if self.state == "intro":
            # The boss remains dormant and cannot be damaged yet.
            self.boss.update(dt, player, tilemap)

            self.state_timer -= dt

            if self.state_timer <= 0:
                self.boss.wake_up()
                self.state = "fight"

            return

        if self.state == "fight":
            self.boss.update(dt, player, tilemap)

            # Check whether Darwin's projectiles hit the boss.
            damage = projectile_manager.check_hit(self.boss.rect)

            if damage > 0:
                self.boss.take_damage(damage)

            # The boss only hurts Darwin during dangerous states.
            if (
                self.boss.hurts_player()
                and player.rect.colliderect(self.boss.rect)
            ):
                player.take_hit(self.boss.rect.centerx)

            # Wait for the boss's defeat animation to finish.
            if self.boss.finished:
                self.state = "cleared"

                tilemap.open_gate()
                tilemap.boss_room_cleared = True

                session.add_score(settings.boss_score)

                self.popup_text = "BOSS DEFEATED"
                self.popup_timer = 2.0

            return

        if self.state == "cleared":
            return

    def draw(self, screen, camera):
        self.boss.draw(screen, camera)

        # Show the victory message near the top of the screen.
        if self.popup_timer > 0:
            font = pygame.font.Font(None, 56)
            image = font.render(
                self.popup_text,
                True,
                (255, 230, 100)
            )

            screen.blit(
                image,
                (
                    settings.screen_width // 2 - image.get_width() // 2,
                    100
                )
            )

    def draw_ui(self, screen):
        # Only show the health bar while the fight is starting
        # or while the boss is still alive.
        if self.state not in ("intro", "fight"):
            return

        bar_width = 500
        bar_height = 24

        bar_x = (settings.screen_width - bar_width) // 2
        bar_y = 35

        # Dark background.
        background_rect = pygame.Rect(
            bar_x,
            bar_y,
            bar_width,
            bar_height
        )

        pygame.draw.rect(
            screen,
            (35, 35, 35),
            background_rect
        )

        # Red health fill.
        health_ratio = self.boss.health / self.boss.max_health
        fill_width = int(bar_width * health_ratio)

        fill_rect = pygame.Rect(
            bar_x,
            bar_y,
            fill_width,
            bar_height
        )

        pygame.draw.rect(
            screen,
            (210, 45, 55),
            fill_rect
        )

        # White outline.
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            background_rect,
            3
        )

        # Boss label.
        font = pygame.font.Font(None, 32)
        label = font.render(
            self.boss.data["label"],
            True,
            (255, 255, 255)
        )

        screen.blit(
            label,
            (
                settings.screen_width // 2 - label.get_width() // 2,
                bar_y + 30
            )
        )

    def reset(self):
        # Recreate the boss with full health.
        self.boss = Boss(
            self.boss_id,
            self.tilemap.boss_spawn,
            self.tilemap
        )

        self.state = "waiting"
        self.state_timer = 0

        self.popup_timer = 0
        self.popup_text = ""

        # Reopen the entrance for another attempt.
        self.tilemap.open_gate()
        self.tilemap.boss_room_cleared = False

    def is_started(self):
        return self.state in ("intro", "fight")

    def is_cleared(self):
        return self.state == "cleared"
