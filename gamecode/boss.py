import pygame, math
from asset_path import asset_path

boss_functions =  {
    "boss_1": "f(x) = mx + b",
    "boss_2": "f(x) = ax^2 + bx + c",
    "boss_3": "f(x) = A sin(Bx)"

}

def parabola_point(origin, target, speed, gravity, t):
    sx, sy = origin
    tx, ty = target

    T = (sx - tx) / speed
    vy = (ty - sy - 0.5 * gravity * T * T) / T

    return (
        sx - speed * t,
        sy + vy * t + 0.5 * gravity * t * t
    )

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, stage_data):
        super().__init__()

        self.boss_type = stage_data["boss"]

        self.original_image = pygame.image.load(asset_path(stage_data["boss_sprite"])).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (160, 180))

        self.dash_frames = [
            pygame.transform.scale(pygame.image.load(asset_path("assets/dash1.png")).convert_alpha(), (160, 180)),

            pygame.transform.scale(pygame.image.load(asset_path("assets/dash2.png")).convert_alpha(), (160, 180))
        ]

        self.image = self.original_image
        self.rect = self.image.get_rect(topleft = (x, y))

        if self.boss_type == "boss_1":
            self.max_health = 100
            self.dash_speed = 850
            self.attack_interval = 2.5
        elif self.boss_type == "boss_2":
            self.max_health = 150
            self.dash_speed = 1050
            self.attack_interval = 2.0
        elif self.boss_type == "boss_3":
            self.max_health = 250
            self.dash_speed = 1300
            self.attack_interval = 1.5

        self.health = self.max_health

        #move
        self.speed = 3
        self.target_x = 950
        self.home_x = x
        self.base_y = self.rect.centery

        #states
        self.state = "hovering"

        self.hover_time = 0
        self.hover_amp = 35
        self.hover_speed = 2.5

        if self.boss_type == "boss_3":
            self.hover_amp = 70
            self.hover_speed = 3
        
        self.pos_x = float(self.rect.x)
        self.dash_phase = "approach"
        self.hanging_timer = 0.0

        self.attack_timer = self.attack_interval
        self.prepare_timer = 0.67

        self.gravity_shift_timer = 4 if self.boss_type == "boss_3" else None
        self.gravity_shift_warning_timer = 0

        self.pending_gravity_scale = None
        self.next_gravity_scale = 0.5

        self.dash_frame_index = 0
        self.dash_animation_speed = 0.08
        self.dash_animation_timer = 0

        self.recover_speed = 500
        self.slash_requested = False
        self.slash_warning_timer = 0
        self.slash_warning_duration = 0.7

        self.player_x = 100
        self.slash_origin = None
        self.slash_target = None

        if self.boss_type == "boss_2":
            self.slash_timer = 4
        elif self.boss_type == "boss_3":
            self.slash_timer = 2.5
        else:
            self.slash_timer = None

    def change_image(self, new_image):
        old_center = self.rect.center

        self.image = new_image
        self.rect = self.image.get_rect(center=old_center)

    def update(self, dt):
        if self.boss_type == "boss_3":

            self.gravity_shift_timer -= dt

            if (
                self.gravity_shift_timer <= 0
                and self.gravity_shift_warning_timer <= 0
            ):
                self.gravity_shift_warning_timer = 1
                self.gravity_shift_timer = 5

            if self.gravity_shift_warning_timer > 0:
                self.gravity_shift_warning_timer -= dt

                if self.gravity_shift_warning_timer <= 0:
                    self.gravity_shift_warning_timer = 0

                    self.pending_gravity_scale = self.next_gravity_scale

                    if self.next_gravity_scale == 0.5:
                        self.next_gravity_scale = 1.5
                    else:
                        self.next_gravity_scale = 0.5
                        
        # Count down the warning before launching a slash
        if self.slash_warning_timer > 0:
            self.slash_warning_timer -= dt

            if self.slash_warning_timer <= 0:
                self.slash_warning_timer = 0
                self.slash_requested = True

        if self.slash_timer is not None and self.state == "hovering":
            self.slash_timer -= dt

            if self.slash_timer <= 0 and self.slash_warning_timer <= 0:
                self.slash_warning_timer = self.slash_warning_duration

                self.slash_origin = self.rect.midleft
                self.slash_target = (self.player_x, 420)

                if self.boss_type == "boss_2":
                    self.slash_timer = 4.5
                else:
                    self.slash_timer = 3

        if self.state == "hovering":
            self.change_image(self.original_image)

            self.hover_time += dt

            hover_y = (
                self.base_y
                + math.sin(self.hover_time * self.hover_speed) * self.hover_amp
            )

            if self.boss_type == "boss_3":
                hover_y = max(90, min(630, hover_y))

            self.rect.centery = round(hover_y)

            self.attack_timer -= dt

            if self.attack_timer <= 0:
                self.state = "preparing"

        elif self.state == "preparing":
            self.change_image(self.original_image)

            self.prepare_timer -= dt

            if self.prepare_timer <= 0:
                self.state = "dashing"

            if self.boss_type == "boss_3":
                self.dash_phase = "approach"
                self.pos_x = float(self.rect.x)

                self.dash_frame_index = 0
                self.dash_animation_timer = 0

                self.change_image(
                    self.dash_frames[self.dash_frame_index]
                )

        elif self.state == "dashing":

            if self.boss_type == "boss_3":

                if self.dash_phase == "approach":

                    stop_x = self.player_x + 320
                    distance = self.pos_x - stop_x

                    if distance < 10:
                        self.pos_x = float(stop_x)
                        self.rect.x = round(self.pos_x)

                        self.state = "hanging"
                        self.hanging_timer = 0.6
                    else:
                        approach_speed = max(
                            140, min(self.dash_speed, 3 * distance)
                        )

                        self.pos_x = max(
                            stop_x,
                            self.pos_x - approach_speed * dt
                        )

                        self.rect.x = round(self.pos_x)

                        if self.pos_x - stop_x < 10:
                            self.pos_x = float(stop_x)
                            self.rect.x = round(self.pos_x)

                            self.state = "hanging"
                            self.hanging_timer = 0.6
                elif self.dash_phase == "lunge":

                    self.pos_x -= self.dash_speed * 1.15 * dt
                    self.rect.x = round(self.pos_x)

            else:
                self.rect.x -= self.dash_speed * dt

            if self.state == "dashing":
                self.dash_animation_timer += dt

                if self.dash_animation_timer >= self.dash_animation_speed:
                    self.dash_animation_timer -= self.dash_animation_speed

                    self.dash_frame_index = (
                        self.dash_frame_index + 1
                    ) % len(self.dash_frames)

                    self.change_image(
                        self.dash_frames[self.dash_frame_index]
                    )

            if self.rect.right < 0:
                self.change_image(self.original_image)
                self.state = "recovering"

        elif self.state == "hanging":
            self.hanging_timer -= dt
            self.image = self.original_image.copy()

            if (pygame.time.get_ticks() // 100) % 2 == 0:
                self.image.set_alpha(90)

            if self.hanging_timer <= 0:
                self.state = "dashing"
                self.dash_phase = "lunge"

                self.dash_frame_index = 0
                self.dash_animation_timer = 0

                self.change_image(
                    self.dash_frames[self.dash_frame_index]
                )
        elif self.state == "recovering":
            self.change_image(self.original_image)

            self.rect.x += self.recover_speed * dt

            if self.rect.left >= self.home_x:
                self.rect.x = self.home_x
                self.rect.centery = self.base_y

                self.state = "hovering"

                self.attack_timer = self.attack_interval
                self.prepare_timer = 0.67
                self.hover_time = 0
                self.dash_phase = "approach"
                self.pos_x = float(self.rect.x)

    def draw_warning(self, screen):
        # Show a warning only while a dash or slash is being prepared
        if self.gravity_shift_warning_timer > 0:
            warning_text = "WARNING! GRAVITY SHIFT!"
        elif self.state == "hanging":
            warning_text = "WARNING LUNGE INCOMING!"
        elif self.state == "preparing":
            warning_text = "WARNING! BOSS DASH INCOMING!"
        elif self.slash_warning_timer > 0:
            warning_text = "WARNING! SLASH INCOMING!"
        else:
            return

        # Alternate the warning color to make it flash
        flash = (pygame.time.get_ticks() // 150) % 2 == 0
        warning_color = (255, 60, 40) if flash else (255, 200, 40)

        # Draw a translucent banner
        warning_surface = pygame.Surface(
            (screen.get_width(), 55),
            pygame.SRCALPHA
        )
        warning_surface.fill((
            warning_color[0],
            warning_color[1],
            warning_color[2],
            65
        ))
        screen.blit(warning_surface, (0, 75))

        pygame.draw.rect(
            screen,
            warning_color,
            (0, 75, screen.get_width(), 55),
            4
        )

        font = pygame.font.Font(None, 42)
        text = font.render(warning_text, True, warning_color)
        text_rect = text.get_rect(
            center=(screen.get_width() // 2, 102)
        )
        screen.blit(text, text_rect)

        if (
            self.boss_type == "boss_2"
            and self.slash_warning_timer > 0
            and self.slash_origin is not None
            and self.slash_target is not None
        ):
            speed = 750
            gravity = 1200

            sx, sy = self.slash_origin
            tx, ty = self.slash_target
            T = (sx - tx) / speed

            for i in range(18):
                t = T * i / 17
                
                x, y = parabola_point(
                    self.slash_origin,
                    self.slash_target,
                    speed,
                    gravity,
                    t
                )

                pygame.draw.circle(
                    screen,
                    (255, 255, 255),
                    (round(x), round(y)),
                    4
                )

    def damage(self, amount):
        self.health = max(0, self.health - amount)

        if self.health <= 0:
            self.kill()

    def health_bar(self, screen):
        bar_width = 300
        bar_height = 20

        bar_x = (screen.get_width() - bar_width) // 2
        bar_y = 30

        pygame.draw.rect(screen, (80,80,80), (bar_x, bar_y, bar_width, bar_height))

        health_ratio = self.health / self.max_health
        health_width = int(bar_width * health_ratio)

        pygame.draw.rect(screen, (220, 40, 40), (bar_x, bar_y, health_width, bar_height))

        function_text = boss_functions.get(self.boss_type, "")

        if function_text:
            font = pygame.font.Font(None, 26)
            label = font.render(function_text, True, (235, 225, 220))
            label_rect = label.get_rect(
                center=(screen.get_width() // 2, bar_y + bar_height + 14)
                )
            screen.blit(label, label_rect)   
        
class SlashAttack(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()

        self.image = pygame.Surface((100, 70), pygame.SRCALPHA)

        pygame.draw.polygon(
            self.image,
            (255, 210, 40),
            [(5, 55), (35, 12), (95, 5), (60, 30), (25, 65)]
        )

        pygame.draw.lines(
            self.image,
            (255, 255, 220),
            False,
            [(20, 50), (43, 25), (75, 15)],
            5
        )

        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.hitbox = self.rect.inflate(-20, -20)

    def update(self, dt):
        self.rect.x -= self.speed * dt

        self.hitbox.center = self.rect.center
        
        if self.rect.right < 0:
            self.kill()

class ParabolaSlash(SlashAttack):
    def __init__(self, origin, target, speed, gravity = 1200):
        super().__init__(origin[0], origin[1], speed)

        self.origin = origin
        self.target = target
        self.speed = speed
        self.gravity = gravity
        self.t = 0

    def update(self, dt):
        self.t += dt

        x, y = parabola_point(
            self.origin,
            self.target,
            self.speed,
            self.gravity,
            self.t
        )

        self.rect.center = (round(x), round(y))
        self.hitbox.center = self.rect.center

        display = pygame.display.get_surface()
        screen_height = display.get_height() if display else 720

        if self.rect.right < 0 or self.rect.top > screen_height:
            self.kill()

    