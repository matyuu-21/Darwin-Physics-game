import pygame

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

    def update(self):
        if self.rect.x > self.target_x:
            self.rect.x -= self.speed

            if self.rect.x < self.target_x:
                self.rect.x = self.target_x

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