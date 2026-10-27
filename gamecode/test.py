import pygame, boss

pygame.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

boss_enemy = boss.Boss(1000, 180)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                boss_enemy.damage(10)

    boss_enemy.update()

    screen.fill((30, 30, 30))

    screen.blit(boss_enemy.image, boss_enemy.rect)
    boss_enemy.health_bar(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()