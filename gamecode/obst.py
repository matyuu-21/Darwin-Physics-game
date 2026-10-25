import pygame, sys, random
from asset_path import asset_path


ground_y = 490

cactus_images = [
    pygame.image.load(asset_path("assets/cacti/cactus1.png")),
    pygame.image.load(asset_path("assets/cacti/cactus2.png")),
    pygame.image.load(asset_path("assets/cacti/cactus3.png")),
    pygame.image.load(asset_path("assets/cacti/cactus4.png")),
    pygame.image.load(asset_path("assets/cacti/cactus5.png")),
    pygame.image.load(asset_path("assets/cacti/cactus6.png"))
]

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        cactus_index = random.randrange(len(cactus_images))
        original_image = cactus_images[cactus_index]

        cactus_sizes = [
            (80, 100),
            (120, 140),
            (100, 120),
            (140, 180),
            (100, 120),
            (140, 180)
        ]

        size = cactus_sizes[cactus_index]
        scaled_image = pygame.transform.scale(original_image, size)

        visible_rect = scaled_image.get_bounding_rect()
        self.image = scaled_image.subsurface(visible_rect).copy()


        self.rect = self.image.get_rect()
        self.rect.midbottom = (1280, ground_y) #height of where the cacti spawns

    def update(self, game_speed):
        self.rect.x -= game_speed

        if self.rect.right < 0:
            self.kill()

class Ptero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.flying_sprites = []

        self.flying_sprites.append(pygame.transform.scale
        (pygame.image.load(asset_path("assets/ptero1.png")), (100, 80)))

        self.flying_sprites.append(pygame.transform.scale
        (pygame.image.load(asset_path("assets/ptero2.png")), (100, 80)))

        self.current_image = 0
        self.image = self.flying_sprites[0]

        self.rect = self.image.get_rect()
        self.rect.x = 1280
        self.rect.y = random.choice([300, 360, 400]) #random height for ptero

    def update(self, game_speed):
        self.current_image += 0.05

        if self.current_image >= len(self.flying_sprites):
            self.current_image = 0

        self.image = self.flying_sprites[int(self.current_image)]

        self.rect.x -= int(game_speed * 1.5) #pteros fly faster than cacti

        if self.rect.right < 0:
            self.kill()