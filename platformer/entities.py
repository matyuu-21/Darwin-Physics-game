import math, pygame, settings

class Coin:
    def __init__(self, col, row):
        coin_x = col * settings.tile + settings.tile / 2
        coin_y = row * settings.tile + settings.tile / 2

        self.pos = pygame.Vector2(coin_x, coin_y)

        self.width = 28
        self.height = 28

        self.rect = pygame.Rect(
            0, 0, self.width, self.height
        )

        self.rect.center = (
            round(self.pos.x),
            round(self.pos.y)
        )

        self.base_y = self.pos.y
        self.bob_timer = 0

        self.collected = False

    def update(self, dt):

        self.bob_timer += dt

        bob_offset = math.sin(self.bob_timer * 2.5) * 5

        self.pos.y = self.base_y + bob_offset
        self.rect.center = (
            round(self.pos.x),
            round(self.pos.y)
        )

    def is_near_camera(self, camera, screen, margin):

        camera_rect = pygame.Rect(
            camera.x - margin, 
            camera.y - margin,
            screen.get_width() + margin * 2,
            screen.get_width() + margin* 2
        )

        return camera_rect.collidedict(self.rect)

    def draw(self, screen, camera):
        pygame.draw.rect(
            screen,
            (255, 215, 0), camera.apply(self.rect)
        )

        pygame.draw.rect(
            screen, (180, 130, 0), camera.apply(self.rect), 2
        )