
import settings
from entities import Projectile


class ProjectileManager:
    def __init__(self):
        self.shots = []
        self.cooldown_timer = 0

    def fire(self, player, manual=False):
        if not settings.shoot_always and not manual:
            return

        if self.cooldown_timer > 0:
            return

        if len(self.shots) >= settings.max_shots:
            return

        self.shots.append(Projectile(player))
        self.cooldown_timer = settings.shot_cooldown

    def update(self, dt, tilemap):
        self.cooldown_timer = max(
            0,
            self.cooldown_timer - dt
        )

        alive_shots = []

        for shot in self.shots:
            shot.update(dt)

            if shot.age >= settings.shot_lifetime:
                shot.alive = False

            if (
                shot.rect.right < 0
                or shot.rect.left > tilemap.width_px
                or shot.rect.bottom < 0
                or shot.rect.top > tilemap.height_px
            ):
                shot.alive = False

            if shot.alive:
                solid_tiles = tilemap.get_solid_tiles(shot.rect)

                for tile_rect in solid_tiles:
                    if shot.rect.colliderect(tile_rect):
                        shot.alive = False
                        break

            if shot.alive:
                alive_shots.append(shot)

        self.shots = alive_shots

    def check_hit(self, target_rect):
        total_damage = 0
        alive_shots = []

        for shot in self.shots:
            if shot.rect.colliderect(target_rect):
                total_damage += shot.damage
                shot.alive = False

            if shot.alive:
                alive_shots.append(shot)

        self.shots = alive_shots
        return total_damage

    def draw(self, screen, camera):
        for shot in self.shots:
            shot.draw(screen, camera)

    def clear(self):
        self.shots.clear()
        self.cooldown_timer = 0
