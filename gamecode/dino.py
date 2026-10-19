import pygame, sys, random

class Dinosaur(pygame.sprite.Sprite): #learn classses
    def __init__(self, x, y):
        super().__init__()

        self.running_sprites = []
        self.ducking_sprites = []

        self.running_sprites.append(pygame.transform.scale(pygame.image.load("assets/run1.png"), (110, 130)))
        self.running_sprites.append(pygame.transform.scale(pygame.image.load("assets/run2.png"), (110, 130)))

        self.ducking_sprites.append(pygame.transform.scale(pygame.image.load("assets/duck.png"), (110, 130)))
        self.ducking_sprites.append(pygame.transform.scale(pygame.image.load("assets/duck.png"), (110, 130)))
      
        self.x = x
        self.y = y
    
        self.current_image = 0
        self.image = self.running_sprites[self.current_image]
        self.rect = self.image.get_rect(center = (x, 360))

        self.y_velocity = 0
        self.gravity = 0.95
        self.jump_strength = -30

        self.is_ducking = False
        self.is_jumping = False

    def update(self):
        self.animate()
        self.apply_gravity()

    def animate(self):
        self.current_image += 0.05

        if self.current_image >= len(self.running_sprites):
            self.current_image = 0

        if self.is_ducking:
            self.image = self.ducking_sprites[int(self.current_image)]
        else:
            self.image = self.running_sprites[int(self.current_image)]

    def duck(self):
        if not self.is_jumping:
            if not self.is_ducking:
                self.is_ducking = True
                self.rect.centery = 380

    def unduck(self):
        if self.is_ducking:
            self.is_ducking = False
            self.rect.centery = 360

    def jump(self):
        if not self.is_jumping and not self.is_ducking:
            self.is_jumping = True
            self.y_velocity = self.jump_strength

    def apply_gravity(self):
        if self.is_jumping:
            self.y_velocity += self.gravity
            self.rect.centery += self.y_velocity

            # Stop the dinosaur when it lands
            if self.rect.centery >= 380:
                self.rect.centery = 380
                self.y_velocity = 0
                self.is_jumping = False