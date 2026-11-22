import pygame, settings
from boss_data import BOSSES

class Boss:
    def __init__(self, boss_id, spawn_point, tilemap):
        self.data = BOSSES[boss_id]

        self.pos = pygame.Vector2(0, 0)
        self.rect = pygame.Rect(
            0, 0, self.data["width"], self.data["height"]
        )

        self.rect.midbottom = spawn_point
        self.pos.update(self.rect.topleft)

        self.room_left = tilemap.boss_room_left + settings.tile
        self.room_right = (
            tilemap.boss_room_left + settings.boss_room_columns * settings.tile
        )

        self.max_health = self.data["health"]
        self.health = self.max_health

        self.facing = -1 #-1 left 1 is right

        self.state = "dormant"
        self.state_timer = 0

        self.hit_flash_timer = 0
        self.finished = False

    def wake_up(self):

        if self.state == "dormant":
            self.state = "idle"
            self.state_timer = self.data["idle_time"]

    def move_horizontal(self, dt, tilemap):
        old_x = self.rect.x

        self.pos.x += self.facing * self.current_speed * dt
        self.rect.x = round(self.pos.x)

        hit_wall = False

        for tile_rect in tilemap.get_solid_tiles(self.rect):
            if self.rect.colliderect(tile_rect):
                hit_wall = True

                if self.facing > 0:
                    self.rect.right = tile_rect.left
                else:
                    self.rect.left = tile_rect.right

                self.pos.x = float(self.rect.x)

        if self.rect.left < self.room_left:
            self.rect.left = self.room_left
            self.pos.x = float(self.rect.x)
            hit_wall = True

        if self.rect.right > self.room_right:
            self.rect.right = self.room_right
            self.pos.x = float(self.rect.x)
            hit_wall = True

        if self.rect.x == old_x and self.current_speed == 0:
            hit_wall = False

        return hit_wall

    def update(self, dt, player, tilemap):
        self.hit_flash_timer = max(
            0, self.hit_flash_timer - dt
        )

        if self.state == "dormant":

            if player.rect.centerx < self.rect.centerx:
                self.facing = -1
            else: 
                self.facing = 1

            return

        if self.state == "dead":
            self.state_timer -= dt
            if self.state_timer <= 0:
                self.finished = True

            return

        if self.state == "idle":
            if player.rect.centerx < self.rect.centerx:
                self.facing = -1
            else:
                self.facing = 1

            self.current_speed = self.data["walk_speed"]
            self.move_horizontal(dt, tilemap)

            self.state_timer -= dt

            if self.state_timer <= 0:
                self.state = "telegraph"
                self.state_timer = self.data["telegraph_time"]

                if player.rect.centerx < self.rect.centerx:
                    self.facing = -1
                else:
                    self.facing = 1

            return

        if self.state == "telegraph":
            self.state_timer -= dt

            if self.state_timer <= 0:
                self.state = "charge"
                self.current_speed = self.data["charge_speed"]

            return

        if self.state == "charge":
            self.current_speed = self.data["charge_speed"]
            hit_wall = self.move_horizontal(dt, tilemap)

            if hit_wall:
                self.state = "recover"
                self.state_timer = self.data["recover_time"]

            return

        if self.state == "recover":
            self.state_timer -= dt

            if self.state_timer <= 0:
                self.state = "idle"
                self.state_timer = self.data["idle_time"]

    def take_damage(self, amount):
        if self.state in ("dormant", "dead") or amount <= 0:
            return

        damage = amount

        if self.state == "recover":
            damage *= self.data["recover_damage_mult"]

        self.health = max(0, self.health - damage)
        self.hit_flash_timer = settings.boss_hit_flash

        if self.health <= 0:
            self.state = "dead"
            self.state_timer = settings.boss_defeat_time

    def hurts_player(self):
        return self.state in (
            "idle",
            "telegraph",
            "charge"
        )

    def draw(self, screen, camera):
        screen_rect = camera.apply(self.rect)

        draw_color = self.data["color"]

        if self.hit_flash_timer > 0:
            draw_color = (255, 255, 255)

        if self.state == "telegraph":
            elapsed = (
                self.data["telegraph_time"] - self.state_timer
            )

            if int(elapsed / 0.1) % 2 == 0:
                draw_color = (255, 80, 80)

        if self.state == "dead":
            progress = (
                self.state_timer / settings.boss_defeat_time
            )

            alpha = max(0, min(255, int(255 * progress)))

            boss_surface = pygame.Surface(
                self.rect.size,
                pygame.SRCALPHA
            )

            pygame.draw.rect(
                boss_surface,
                (*draw_color, alpha),
                boss_surface.get_rect()
            )

            pygame.draw.rect(
                boss_surface,
                (40, 20, 20, alpha),
                boss_surface.get_rect(),
                4
            )

            screen.blit(boss_surface, screen_rect)
            return

        pygame.draw.rect(
            screen,
            draw_color,
            screen_rect
        )

        pygame.draw.rect(
            screen,
            (40, 20, 20),
            screen_rect,
            4
        )

        # Simple eyes show which direction the boss is facing.
        eye_x = screen_rect.centerx + self.facing * 25
        eye_y = screen_rect.top + 35

        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (eye_x, eye_y),
            9
        )

        pygame.draw.circle(
            screen,
            (20, 20, 20),
            (eye_x, eye_y),
            4
        )

        # Show an exclamation mark during the charge warning.
        if self.state == "telegraph":
            font = pygame.font.Font(None, 64)
            warning = font.render("!", True, (255, 40, 40))

            screen.blit(
                warning,
                (screen_rect.centerx - warning.get_width() // 2,
                 screen_rect.top - 55)
            )
