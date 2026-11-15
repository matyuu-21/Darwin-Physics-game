import pygame

class Pipe(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((85, 130), pygame.SRCALPHA)

        pygame.draw.rect(
            self.image,
            (30, 170, 60),
            (12, 20, 60, 110),
        )

        pygame.draw.rect(
            self.image,
            (15, 90, 35),
            (12, 20, 60, 110),
            4
        )

        pygame.draw.rect(
            self.image,
            (40, 210, 35),
            (0, 0, 85, 35),
        )

        pygame.draw.rect(
            self.image,
            (15, 90, 35),
            (0, 0, 85, 35),
            4
        )

        self.rect = self.image.get_rect()
        self.rect.midbottom = (1280, 480)
        self.pos_x = float(self.rect.x)

    def update(self, game_speed):
        self.pos_x -= game_speed
        self.rect.x = round(self.pos_x)

        if self.rect.right < 0:
            self.kill()

class BonusCoin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)

        pygame.draw.circle(self.image, (255, 190, 0), (15, 15), 13)
        pygame.draw.circle(self.image, (255, 235, 80), (15, 15), 9)
        pygame.draw.circle(self.image, (255, 255, 180), (11, 10), 3)

        self.rect = self.image.get_rect(center=(x, y))
        self.pos_x = float(self.rect.x)

    def update(self, game_speed):
        self.pos_x -= game_speed
        self.rect.x = round(self.pos_x)

        if self.rect.right < 0:
            self.kill