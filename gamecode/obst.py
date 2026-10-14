import pygame, sys, random

cactus_images = [
    pygame.image.load("assets/cacti/cactus1.png"),
    pygame.image.load("assets/cacti/cactus2.png"),
    pygame.image.load("assets/cacti/cactus3.png"),
    pygame.image.load("assets/cacti/cactus4.png"),
    pygame.image.load("assets/cacti/cactus5.png"),
    pygame.image.load("assets/cacti/cactus6.png")
]

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        original_image = random.choice(cactus_images)
        self.image = pygame.transform.scale(original_image, (100,120))

        self.rect = self.image.get_rect()
        self.rect.midbottom = (1280, 400) #height of where the cacti spawns

    def update(self, game_speed):
        self.rect.x -= game_speed

        if self.rect.right < 0:
            self.kill()

class Ptero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.flying_sprites = []

        self.flying_sprites.append(pygame.transform.scale
        (pygame.image.load("assets/ptero1.png"), (100, 80)))

        self.flying_sprites.append(pygame.transform.scale
        (pygame.image.load("assets/ptero2.png"), (100, 80)))

        self.current_image = 0
        self.image = self.flying_sprites[0]

        self.rect = self.image.get_rect()
        self.rect.x = 1280
        self.rect.y = random.choice([250, 300, 350]) #random height for ptero

    def update(self, game_speed):
        self.current_image += 0.05

        if self.current_image >= len(self.flying_sprites):
            self.current_image = 0

        self.image = self.flying_sprites[int(self.current_image)]

        self.rect.x -= int(game_speed * 1.5) #pteros fly faster than cacti

        if self.rect.right < 0:
            self.kill()