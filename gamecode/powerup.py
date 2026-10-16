import pygame, random

class PowerUp(pygame.sprite.Sprite):
    TYPES = ["heart", "shield", "double_score"]
#replace w pic assets next week
    COLORS = {
        "heart": (235, 55, 75),
        "shield": (50, 150, 25), 
        "double_score": (255, 190, 40)
    }

    def __init__(self, screen_width=1280):
        super().__init__()

        self.power_type = random.choice(self.TYPES)
        self.size = 35

        self.image = pygame.Surface(
            (self.size, self.size), pygame.SRCALPHA
        )

        pygame.draw.circle(
            self.image, self.COLORS[self.power_type],
            (self.size // 2, self.size // 2), self.size // 2
        )

        #letter identification for power ups temporary
        font = pygame.font.Font(None, 24)
        labels = {
            "heart": "H",
            "shield": "S",
            "double_score": "2x"
        }

        label = font.render(
            labels[self.power_type], True, (255, 255, 255)
        )

        self.image.blit(
            label, label.get_rect(center=(self.size // 2, self.size // 2))
        )

        self.rect = self.image.get_rect()
        self.rect.left = screen_width
        self.rect.centery = random.choice([250, 300, 330])

    def update(self, game_speed):
        self.rect.x -= int(game_speed)

        if self.rect.right < 0:
            self.kill()