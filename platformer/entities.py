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


class Projectile:
    def __init__(self, player):
        self.direction = player.facing

        self.width = settings.shot_width
        self.height = settings.shot_height

        if self.direction > 0:
            start_x = player.rect.right
        else:
            start_x = player.rect.left - self.width

        start_y = player.rect.top + 30

        self.pos = pygame.Vector2(start_x, start_y)

        self.rect = pygame.Rect(
            round(self.pos.x),
            round(self.pos.y),
            self.width,
            self.height
        )

        self.age = 0
        self.damage = 1
        self.alive = True

    def update(self, dt):
        self.pos.x += (
            settings.shot_speed * self.direction * dt
        )

        self.rect.x = round(self.pos.x)
        self.age += dt

    def draw(self, screen, camera):
        screen_rect = camera.apply(self.rect)

        pygame.draw.rect(
            screen, (255, 220, 40), screen_rect
        )

        pygame.draw.rect(
            screen, (160, 110, 0), screen_rect, 2
        )
