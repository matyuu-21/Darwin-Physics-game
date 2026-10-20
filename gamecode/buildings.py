import pygame, random

class Building(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image =  pygame.image.load("assets/build.png").convert_alpha()

        self.image = pygame.transform.scale(self.image, (180, 200))

        self.rect = self.image.get_rect()
        self.rect.left - 1200
        self.rect.bottom = 360

        self.gap = random.randint(180, 350)

    def update(self, speed):
        self.rect.x -= speed

        if self.rect.right < 0:
            self.kill()