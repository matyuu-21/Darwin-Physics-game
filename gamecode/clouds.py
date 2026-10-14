import pygame, sys, random

cloud_image = pygame.image.load("assets/cloud.png")
cloud_image = pygame.transform.scale(cloud_image, (100, 60))

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = cloud_image

        self.rect = self.image.get_rect()
        self.rect.x = 1280
        self.rect.y = random.randint(50, 200)

        self.speed = random.uniform(1, 3)

    def update(self):
        self.rect.x -= self.speed

        if self.rect.right < 0:
            self.kill()