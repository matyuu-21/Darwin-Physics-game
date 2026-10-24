import pygame, random
from asset_path import asset_path

class Building(pygame.sprite.Sprite):
    def __init__(self, start_x=1280):
        super().__init__()

        image = pygame.image.load(
            asset_path("assets/build.png")
        ).convert_alpha()

        self.image = pygame.transform.scale(image, (280, 200))
        self.rect = self.image.get_rect()

        self.rect.left = start_x
        self.rect.bottom = 320

    def update(self, speed):
        self.rect.x -= speed

        if self.rect.right < 0:
            self.kill()