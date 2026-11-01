import pygame
from asset_path import asset_path

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load(asset_path("assets/projectile.png")).convert_alpha()

        self.iamge = pygame.transform.scale(self.image, (40, 24))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.speed = 10
        self.damage = 10

    def update(self):
        self.rect.x += self.speed

        if self.rect.left > 1280:
            self.kill()