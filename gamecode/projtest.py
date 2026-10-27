import pygame
from projectile import Projectile

pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("projectiletest")

clock = pygame.time.Clock()

projectile_group = pygame.sprite.Group()
projectile_group.add(Projectile(100, 360))

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    projectile_group.update()

    screen.fill((30, 30, 50))
    projectile_group.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()