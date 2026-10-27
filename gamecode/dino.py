import pygame, sys, random
from asset_path import asset_path

ground_y = 420


class Dinosaur(pygame.sprite.Sprite): #learn classses
    def __init__(self, x, y):
        super().__init__()

        self.running_sprites = []
        self.jumping_sprite = pygame.transform.scale(pygame.image.load(asset_path("assets/jump1.png")),(120, 140))

        self.running_sprites.append(pygame.transform.scale(pygame.image.load(asset_path("assets/run1.png")), (120, 140)))
        self.running_sprites.append(pygame.transform.scale(pygame.image.load(asset_path("assets/run2.png")), (120, 140)))

        self.ducking_sprite = pygame.transform.scale(pygame.image.load(asset_path("assets/duck.png")), (120, 125))
    
      
        self.x = x
        self.y = y
    
        self.current_image = 0
        self.image = self.running_sprites[self.current_image]
        self.rect = self.image.get_rect(center = (x + 30, ground_y))

        self.y_velocity = 0
        self.gravity = 0.95
        self.jump_normal = -30
        self.jump_strength = self.jump_normal
        self.jump_timer = 0

        self.is_ducking = False
        self.is_jumping = False

    def update(self, dt):
        self.animate()
        self.apply_gravity()

        if self.jump_timer > 0:
            self.jump_timer -= dt

            if self.jump_timer <= 0:
                self.jump_strength = self.jump_normal

    def animate(self):
        self.current_image += 0.05

        if self.current_image >= len(self.running_sprites):
            self.current_image = 0

        if self.is_ducking:
            self.image = self.ducking_sprite
        elif self.is_jumping:
            self.image = self.jumping_sprite
        else:
            self.image = self.running_sprites[int(self.current_image)]

    def duck(self):
        if not self.is_jumping:
            if not self.is_ducking:
                self.is_ducking = True
                self.rect.centery = ground_y + 35

    def unduck(self):
        if self.is_ducking:
            self.is_ducking = False
            self.rect.centery = ground_y

    def jump(self):
        if not self.is_jumping and not self.is_ducking:
            self.is_jumping = True
            self.y_velocity = self.jump_normal

    def apply_gravity(self):
        if self.is_jumping:
            self.y_velocity += self.gravity
            self.rect.centery += self.y_velocity

            # Stop the dinosaur when it lands
            if self.rect.centery >= ground_y:
                self.rect.centery = ground_y
                self.y_velocity = 0
                self.is_jumping = False

    def get_hitbox(self):
        if self.is_ducking:
            return self.rect.inflate(-30, -25)

        return self.rect.inflate(-35, -30)