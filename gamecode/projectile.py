import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface((20, 10))
        self.image.fill((50, 200, 255))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.speed = 10
        self.damage = 10

    def update(self):
        self.rect.x += self.speed

        if self.rect.left > 1280:
            self.kill