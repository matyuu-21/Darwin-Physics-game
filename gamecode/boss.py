import pygame, math
from asset_path import asset_path

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

        self.attack_timer = self.attack_interval
        self.prepare_timer = 0.67

        self.dash_frame_index = 0
        self.dash_animation_speed = 0.08
        self.dash_animation_timer = 0

        self.recover_speed = 500
        self.slash_requested = False

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

        if self.slash_timer is not None and self.state == "hovering":
            self.slash_timer -= dt

            if self.slash_timer <= 0:
                self.slash_requested = True

                if self.boss_type == "boss_2":
                    self.slash_timer = 4.5
                else:
                    self.slash_timer = 3

        if self.state == "hovering":
            self.change_image(self.original_image)

            self.hover_time += dt

            self.rect.centery = (
                self.base_y + math.sin(self.hover_time * self.hover_speed) * self.hover_amp
            )

            self.attack_timer -= dt

            if self.attack_timer <= 0:
                self.state = "preparing"

        elif self.state == "preparing":
            self.change_image(self.original_image)

            self.prepare_timer -= dt

            if self.prepare_timer <= 0:
                self.state = "dashing"

                self.dash_frame_index = 0
                self.dash_animation_timer = 0

                self.change_image(
                    self.dash_frames[self.dash_frame_index]
                )

        elif self.state == "dashing":
            self.rect.x -= self.dash_speed * dt

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