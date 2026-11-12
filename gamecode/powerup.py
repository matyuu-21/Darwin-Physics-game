import pygame, random
from assets import load_image 

class PowerUp(pygame.sprite.Sprite):
    TYPES = ["heart", "shield", "double_score", "super_jump", "rainbow_star"]
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
            "super_jump": "assets/superjump.png",
            "rainbow_star": "assets/starup.png"
        }

        self.power_type = random.choices(self.TYPES,
            weights=[25,25,20,20,10], k=1
            )[0]

        self.image = load_image(powerup_images[self.power_type], (100, 100))

        self.rect = self.image.get_rect(midleft=(1280, random.randint(320, 420)))

    def update(self, game_speed):
        self.rect.x -= int(game_speed)

        if self.rect.right < 0:
            self.kill()