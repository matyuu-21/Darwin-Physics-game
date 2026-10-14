# sir darwin game lets go
import pygame, sys, random

import dino
import obst
import clouds 

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
pygame.display.set_caption("Darwin's-Journey")

game_font = pygame.font.Font(None, 40)

#groups
dinosaur_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()
cloud_group = pygame.sprite.Group()
ptero_group = pygame.sprite.Group()

#object
dinosaur = dino.Dinosaur(50, 360)
dinosaur_group.add(dinosaur)

#variables for features
game_speed = 5
game_over = False

#ground stuff
ground = pygame.image.load("assets/ground.png") #ground png file
ground = pygame.transform.scale(ground, (1280, 20))
ground_x = 0
ground_rect = ground.get_rect(center = (640, 400))

#spawn timers
SPAWN_OBSTACLE = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_OBSTACLE, 1500)

SPAWN_CLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWN_CLOUD, 3000)

SPAWN_PTERO = pygame.USEREVENT + 3
pygame.time.set_timer(SPAWN_PTERO, 5000)

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

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_UP):
                dinosaur.jump()

        if event.type == SPAWN_OBSTACLE:
            obstacle = obst.Obstacle()
            obstacle_group.add(obstacle)

        if event.type == SPAWN_CLOUD:
            cloud = clouds.Cloud()
            cloud_group.add(cloud)

        if event.type == SPAWN_PTERO:
            ptero = obst.Ptero()
            ptero_group.add(ptero)

    dinosaur_group.update()
    cloud_group.update()

    for obstacle in obstacle_group:
        obstacle.update(game_speed)

    for ptero in ptero_group:
        ptero.update(game_speed)

    screen.fill((255, 255, 255))

    cloud_group.draw(screen)

    dinosaur_group.draw(screen)
    obstacle_group.draw(screen)
    ptero_group.draw(screen)

    if (
        pygame.sprite.spritecollideany(dinosaur, obstacle_group) 
        or pygame.sprite.spritecollideany(dinosaur, ptero_group)
    ):
        print("Game Over")
        pygame.quit()
        sys.exit()

    game_speed += 0.0015
    ground_x -= game_speed

    screen.blit(ground, (ground_x, 360))
    screen.blit(ground, (ground_x + 1280, 360))

    if ground_x <= -1280:
        ground_x = 0

    pygame.display.update()
    clock.tick(120)