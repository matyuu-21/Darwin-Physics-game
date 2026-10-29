import pygame, boss, projectile, dino

pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("testing boss")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

boss_group = pygame.sprite.Group()
projectile_group = pygame.sprite.Group()
dinosaur = dino.Dinosaur(50, 400)
dinosaur_group = pygame.sprite.Group(dinosaur)

boss_enemy = boss.Boss(1000, 180)
boss_group.add(boss_enemy)

running = True

while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f and boss_group:
                shot = projectile.Projectile(
                    dinosaur.rect.right,
                    dinosaur.rect.centery
                )
                projectile_group.add(shot)

    dinosaur_group.update(dt)
    boss_group.update()
    projectile_group.update()

    for shot in list(projectile_group):
        hits = pygame.sprite.spritecollide(
            shot, boss_group, False
                    )

        if hits:
            hit_boss = hits[0]

            hit_boss.take_damage(shot.damage)
            shot.kill()

    screen.fill((30, 30, 50))

    boss_group.draw(screen)
    projectile_group.draw(screen)
    dinosaur_group.draw(screen)

    if boss_group:
        boss_enemy.health_bar(screen)
    else:
        victory = font.render(
            "boss dead", True, (100, 255, 100)
        )
        screen.blit(victory, (500, 350))

    instructions = font.render(
        "F to shoot", True, (255, 255, 255)
    )
    screen.blit(instructions, (30, 30))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()