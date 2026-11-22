import math, pygame, settings

class Player:
    def __init__(self, spawn_point):
        self.pos = pygame.Vector2(spawn_point)
        self.vel = pygame.Vector2(0, 0)

        self.rect = pygame.Rect(
            round(self.pos.x),
            round(self.pos.y),
            settings.player_width,
            settings.player_height
        )

        self.on_ground = False
        self.facing = 1 #right is 1 -1 is left

        self.gravity_scale = settings.PLANETS["EARTH"]
        self.planet_name = "EARTH"

        self.coyote_timer = 0
        self.jump_buffer_timer = 0

        self.jump_cut_used = False

        self.lives = settings.max_lives
        self.invincible_timer = 0
        self.fell_out = False

    def set_planet(self, name):
        name = name.upper()

        if name in settings.PLANETS:
            self.planet_name = name
            self.gravity_scale = settings.PLANETS[name]

    def respawn(self, spawn_point):
        self.pos.update(spawn_point)
        self.vel.update(0,0)

        self.rect.topleft = (
            round(self.pos.x),
            round(self.pos.y)
        )

        self.on_ground = False
        self.coyote_timer = 0
        self.jump_buffer_timer = 0
        self.jump_cut_used = False

    def take_hit(self, source_x):
        if self.invincible_timer > 0 or self.lives <= 0:
            return False

        self.lives -= 1
        self.invincible_timer = settings.invincible_time

        direction = 1 if self.pos.x >= source_x else -1
        self.vel.x = direction * settings.hit_knockback_x
        self.vel.y = settings.hit_knockback_y

        self.on_ground = False

        return True
    
    def handle_event(self, event):
        jump_keys = (
            pygame.K_SPACE,
            pygame.K_UP,
            pygame.K_w
        )

        if event.type == pygame.KEYDOWN:
            if event.key in jump_keys:
                self.jump_buffer_timer = settings.jump_buffer

            elif event.key == pygame.K_1:
                self.set_planet("EARTH")
            elif event.key == pygame.K_2:
                self.set_planet("MOON")
            elif event.key == pygame.K_3:
                self.set_planet("JUPITER")

        elif event.type == pygame.KEYUP:
            if event.key in jump_keys:

                if self.vel.y < 0 and not self.jump_cut_used:
                    self.vel.y *= settings.jump_cut
                    self.jump_cut_used = True

    def get_jump_speed(self):
        if settings.gravity_jump_mode == "same_height":
            return settings.jump_speed * math.sqrt(self.gravity_scale)

        return settings.jump_speed

    def move_towards(self, current, target, amount):
        if current < target:
            return min(current + amount, target)

        if current > target:
            return max(current - amount, target)

        return current

    def update(self, dt, keys, tilemap):
        self.invincible_timer = max(0, self.invincible_timer - dt)
        dt = min(dt, 1 / 30)

        if self.on_ground:
            self.coyote_timer = settings.coyote_time
        else:
            self.coyote_timer = max(0, self.coyote_timer - dt)

        self.jump_buffer_timer = max(
            0, self.jump_buffer_timer - dt
        )

        move_direction = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            move_direction -= 1

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            move_direction += 1

        if move_direction != 0:
            self.facing = move_direction

            if self.on_ground:
                acceleration = settings.ground_accel
            else:
                acceleration = settings.air_accel

            if self.vel.x * move_direction < 0:
                acceleration *= settings.turn_boost

            self.vel.x += move_direction * acceleration * dt

            self.vel.x = max(
                -settings.max_run,
                min(settings.max_run, self.vel.x)
            )

        else:
            if self.on_ground:
                friction = settings.ground_friction
            else:
                friction = settings.air_accel

            self.vel.x = self.move_towards(
                self.vel.x,
                0, friction * dt
            )

        if self.jump_buffer_timer > 0 and self.coyote_timer > 0:
            self.vel.y = -self.get_jump_speed()

            self.on_ground = False
            self.coyote_timer = 0
            self.jump_buffer_timer = 0
            self.jump_cut_used = False

        gravity = settings.earth_gravity * self.gravity_scale

        if self.vel.y > 0:
            gravity *= settings.fall_mult
        self.vel.y += gravity * dt

        self.vel.y = min(self.vel.y, settings.max_fall)

        # x axis colis
        self.pos.x += self.vel.x * dt
        self.rect.x = round(self.pos.x)

        for tile_rect in tilemap.get_solid_tiles(self.rect):
            if self.rect.colliderect(tile_rect):
                if self.vel.x > 0:
                    self.rect.right = tile_rect.left
                elif self.vel.x < 0:
                    self.rect.left = tile_rect.right

                self.pos.x = float(self.rect.x)
                self.vel.x = 0

        # y collis
        self.on_ground = False

        self.pos.y += self.vel.y * dt
        self.rect.y = round(self.pos.y)

        for tile_rect in tilemap.get_solid_tiles(self.rect):
            if self.rect.colliderect(tile_rect):
                if self.vel.y > 0:
                    self.rect.bottom = tile_rect.top    
                    self.on_ground = True

                    self.coyote_timer = settings.coyote_time

                elif self.vel.y < 0:
                    self.rect.top = tile_rect.bottom

                self.pos.y = float(self.rect.y)
                self.vel.y = 0

        #respawning

        if self.pos.y > tilemap.height_px + settings.tile:
            self.fell_out = True

    def draw(self, screen, camera):
        if self.invincible_timer > 0:
            if int(self.invincible_timer * 10) % 2 == 0:
                return

        screen_rect = camera.apply(self.rect)
        pygame.draw.rect(screen, (255, 140, 0), screen_rect)