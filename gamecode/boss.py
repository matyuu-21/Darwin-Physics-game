import pygame, math
from asset_path import asset_path

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.original_image = pygame.image.load(asset_path("assets/boss1.png")).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (160, 180))

        self.dash_frames = [
            pygame.transform.scale(pygame.image.load(asset_path("assets/dash1.png")).convert_alpha(), (160, 180)),

            pygame.transform.scale(pygame.image.load(asset_path("assets/dash2.png")).convert_alpha(), (160, 180))
        ]

        self.image = self.original_image
        self.rect = self.image.get_rect(topleft = (x, y))

        #health
        self.max_health = 100
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

        self.attack_timer = 2.5
        self.prepare_timer = 0.67

        self.dash_speed = 850
        self.dash_frame_index = 0
        self.dash_animation_speed = 0.08

        self.recover_speed = 500

    def change_image(self, new_image):
        old_center = self.rect.center

        self.image = new_image
        self.rect = self.image.get_rect(center=old_center)

    def update(self, dt):

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

                self.attack_timer = 3
                self.prepare_timer = 0.67
                self.hover_tiome = 0

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

