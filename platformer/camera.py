import math, pygame, settings

class Camera:
    def __init__(self, level_width, level_height):
        self.x = 0
        self.y = 0

        self.level_width = level_width
        self.level_height = level_height

        self.screen_width = settings.screen_width
        self.screen_height = settings.screen_height

        self.locked_x = None

    def clamp_position(self, x, y):
        max_x = max(0, self.level_width - self.screen_width)
        max_y = max(0, self.level_height - self.screen_height)

        x = max(0, min(x, max_x))
        y = max(0, min(y, max_y))

        return x, y

    def update(self, player, dt):
        dt = min(dt, 1 / 36)

        #horizontal following

        if self.locked_x is not None:
            target_x = self.locked_x
        else:
            target_x = (
                player.rect.centerx
                - self.screen_width / 2
                + player.facing * settings.camera_look_ahead
            )
        #vert deadzone

        dead_zone_top = self.screen_height / 2 - settings.camera_dead_zone
        dead_zone_bottom = self.screen_height / 2 + settings.camera_dead_zone

        player_screen_y = player.rect.centery - self.y

        target_y = self.y

        if player_screen_y < dead_zone_top:
            target_y = player.rect.centery - dead_zone_top
        elif player_screen_y > dead_zone_bottom:
            target_y = player.rect.centery - dead_zone_bottom

        target_x, target_y = self.clamp_position(target_x, target_y)

        #keeps stuff smooth consistently
        smooth_amount = 1 - math.exp(-settings.camera_smooth * dt)

        self.x += (target_x - self.x) * smooth_amount
        self.y += (target_y - self.y) * smooth_amount

        self.x, self.y = self.clamp_position(self.x, self.y)

    def apply(self, rect):
        return rect.move((
            -round(self.x),
            -round(self.y)
        ))

    def world_to_screen(self, pos):
        return pygame.Vector2(
            pos[0] - self.x,
            pos[1] - self.y
        )

    def lock_to(self, x):
        self.locked_x = x

    def unlock(self):
        self.locked_x = None