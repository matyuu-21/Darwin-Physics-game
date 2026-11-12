
import pygame, random
from assets import load_image

ground_y = 490

# Dimensions of each cactus
CACTUS_SIZES = [
    (160, 180),
    (140, 160),
    (120, 140),
    (140, 180),
    (140, 160),
    (180, 160)
]

# Cache for loaded cactus images
_cactus_cache = {}

def _cactus_surface(i):
    if i not in _cactus_cache:
        img = load_image(
            f"assets/cacti/cactus{i + 1}.png",
            CACTUS_SIZES[i]
        )

        # Remove transparent padding
        _cactus_cache[i] = img.subsurface(
            img.get_bounding_rect()
        ).copy()

    return _cactus_cache[i]


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Select one random cactus
        cactus_index = random.randrange(len(CACTUS_SIZES))

        # Load its cached image
        self.image = _cactus_surface(cactus_index)

        self.rect = self.image.get_rect()
        self.rect.midbottom = (1280, ground_y)

        # More precise movement
        self.pos_x = float(self.rect.x)

        # Smaller collision area
        self.hitbox = self.rect.inflate(-30, -10)

    def update(self, game_speed):
        self.pos_x -= game_speed
        self.rect.x = round(self.pos_x)

        # Keep the hitbox attached to the cactus
        self.hitbox.center = self.rect.center

        if self.rect.right < 0:
            self.kill()


class Ptero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load and cache both flying animation frames
        self.flying_sprites = [
            load_image("assets/ptero1.png", (100, 80)),
            load_image("assets/ptero2.png", (100, 80))
        ]

        self.current_image = 0
        self.image = self.flying_sprites[0]

        self.rect = self.image.get_rect()
        self.rect.x = 1280
        self.rect.y = random.choice([300, 360, 400])

        # More precise movement
        self.pos_x = float(self.rect.x)

    def update(self, game_speed):
        # Animate the ptero
        self.current_image += 0.05

        if self.current_image >= len(self.flying_sprites):
            self.current_image = 0

        self.image = self.flying_sprites[int(self.current_image)]

        # Pteros fly 1.5 times faster than cacti
        self.pos_x -= game_speed * 1.5
        self.rect.x = round(self.pos_x)

        if self.rect.right < 0:
            self.kill()
