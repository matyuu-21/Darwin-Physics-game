# sir darwin game lets go
import pygame, sys, random

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
pygame.display.set_caption("Darwin's-Journey")

game_font = pygame.font.Font(None, 40)

#dinosaur class
class Dinosaur(pygame.sprite.Sprite): #learn classses
    def __init__(self, x, y):
        super().__init__()

        self.running_sprites = []
        self.ducking_sprites = []

        self.running_sprites.append(pygame.transform.scale(pygame.image.load("assets/dino1.png"), (80, 100)))
        self.running_sprites.append(pygame.transform.scale(pygame.image.load("assets/dino2.png"), (80, 100)))

        self.ducking_sprites.append(pygame.transform.scale(pygame.image.load("assets/dinoducking1.png"), (80, 100)))
        self.ducking_sprites.append(pygame.transform.scale(pygame.image.load("assets/dinoducking2.png"), (80, 100)))
       
        self.x = x
        self.y = y
    
        self.current_image = 0
        self.image = self.running_sprites[self.current_image]
        self.rect = self.image.get_rect(center = (x, y))

        self.velocity = 50
        self.gravity = 4.5
        self.is_ducking = False
        self.jump = False

    def update(self):
        self.animate()
        self.apply_gravity()

    def animate(self):
        self.current_image += 0.05

        if self.current_image > 1:
            self.current_image = 0

        if self.is_ducking:
            self.image = self.ducking_sprites[int(self.current_image)]
        else:
            self.image = self.running_sprites[int(self.current_image)]

    def duck(self):
        self.is_ducking = True
        self.rect.centery = 380

    def unduck(self):
        self.is_ducking = False
        self.rect.centery = 360

    def apply_gravity(self):
        if self.rect.centery <= 360:
            self.rect.centery += self.gravity

    def jump(self):
        if self.rect.centery >= 360:
            while self.rect.centery - self.velocity > 40:
                self.rect.centery -= 1

#groups
dinosaur_group = pygame.sprite.Group()

#object
dinosaur = Dinosaur(50, 360)
dinosaur_group.add(dinosaur)

#variables for features
game_speed = 5

#ground stuff
ground = pygame.image.load("assets/ground.png") #ground png file
ground = pygame.transform.scale(ground, (1280, 20))
ground_x = 0
ground_rect = ground.get_rect(center = (640, 400))

#mainloop
while True: 
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        dinosaur.duck()
    else:
        if dinosaur.is_ducking:
            dinosaur.unduck()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill("white")
    dinosaur_group.update()
    dinosaur_group.draw(screen)

    game_speed += 0.0015

    ground_x -= 1
    screen.blit(ground, (ground_x, 360))
    screen.blit(ground, (ground_x + 1200, 360))

    if ground_x <= -1280:
        ground_x = 0 

    pygame.display.update()
    clock.tick(120)