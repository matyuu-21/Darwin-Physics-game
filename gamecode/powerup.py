import pygame, random
from asset_path import asset_path

class PowerUp(pygame.sprite.Sprite):
    TYPES = ["heart", "shield", "double_score", "super_jump"]
#replace w pic assets next week
    COLORS = {
        "heart": (235, 55, 75),
    }

    def __init__(self, screen_width=1280):
        super().__init__()

        powerup_images = {
            "heart": "assets/ice_candy.png",
            "shield": "assets/shield.png",
            "double_score": "assets/doublescore.png",
            "super_jump": "assets/superjump.png"
        }

        self.power_type = random.choice(self.TYPES)

        self.image = pygame.image.load(
            asset_path(powerup_images[self.power_type])
        ).convert_alpha()

        self.image = pygame.transform.scale(self.image, (100, 100))

        self.rect = self.image.get_rect(midleft=(1280, random.randint(250, 330)))

    def update(self, game_speed):
        self.rect.x -= int(game_speed)

        if self.rect.right < 0:
            self.kill()