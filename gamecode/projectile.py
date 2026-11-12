import pygame
from assets import load_image

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, score):
        super().__init__()

        self.image = load_image("assets/projectile.png", (65, 40))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.speed = 10
        bonus_damage = int(score // 100) #make it // 2000 if scores back to normal
        self.damage = min(10 + bonus_damage, 14)

    def update(self):
        self.rect.x += self.speed

        if self.rect.left > 1280:
            self.kill()