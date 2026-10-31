import pygame, math

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface((160, 180))
        self.image.fill((180, 50, 50))

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.max_health = 100
        self.health = self.max_health

        self.speed = 3
        self.target_x = 950

        self.home_x = x
        self.base_y = self.rect.centery

        self.state = "hovering"

        self.hover_time = 0
        self.hover_amp = 35
        self.hover_speed = 2.5

        self.attack_timer = 2.5
        self.prepare_timer = 0.67 #67777777777777

        self.dash_speed = 850
        self.dash_angle = 0

        self.recover_speed = 500

        self.original_image = self.image

    def update(self, dt):
        if self.state == "hovering":
            self.hover_time += dt

            self.rect.centery = (
                self.base_y
                + math.sin(self.hover_time * self.hover_speed)
                * self.hover_amp
            )

            self.attack_timer -= dt

            if self.attack_timer <= 0:
                self.state = "preparing"

        elif self.state == "preparing":
            self.prepare_timer -= dt
            if self.prepare_timer <= 0:
                self.state = "dashing"

        elif self.state == "dashing":
            self.rect.x -= self.dash_speed * dt
            self.dash_angle += 720 * dt

            self.image = pygame.transform.rotate(
                self.original_image, self.dash_angle
            )

            old_center = self.rect.center
            self.rect = self.image.get_rect(center=old_center)

            if self.rect.right < 0:
                self.image = self.original_image
                self.rect = self.image.get_rect(center=self.rect.center)

                self.state = "recovering"

        elif self.state == "recovering":
            self.rect.x += self.recover_speed * dt

            if self.rect.left >= self.home_x:

                self.rect.x = self.home_x
                self.rect.centery = self.base_y

                self.state = "hovering"
                self.attack_timer = 3
                self.prepare_timer = 0.67
                self.hover_time = 0

    def damage(self, amount):
        self.health = max(0, self.health - amount)
        if self.health <= 0:
            self.kill()

    def health_bar(self, screen):
        bar_width = 300
        bar_height = 20

        bar_x = (screen.get_width() -  bar_width) // 2
        bar_y = 30

        pygame.draw.rect(screen, (80, 80, 80),
            (bar_x, bar_y, bar_width, bar_height))

        health_ratio = self.health / self.max_health
        health_width = int(bar_width * health_ratio)
        
        pygame.draw.rect(screen, (220, 40, 40),
            (bar_x, bar_y, health_width, bar_height))