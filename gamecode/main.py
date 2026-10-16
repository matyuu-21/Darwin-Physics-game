import pygame, sys, random

import dino, obst, clouds

pygame.init()

#screen variables
screen_width = 1280
screen_height = 720

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
pygame.display.set_caption("darwin laptop")

game_font = pygame.font.Font(None, 40)
title_font = pygame.font.Font(None, 90)
small_font = pygame.font.Font(None, 30)

black = (25, 30, 40)
white = (255, 255, 255)
orange = (255, 145, 50)
dark_orange = (220, 105, 25)
gray = (110, 115, 125)

#groups 
dinosaur_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()
cloud_group = pygame.sprite.Group()
ptero_group = pygame.sprite.Group()

#ground variables
ground = pygame.image.load("assets/ground.png")
ground = pygame.transform.scale(ground, (screen_width, 20))
ground_y = 360
ground_x = 0

game_speed = 5
score = 0 
best_score = 0
game_state = "menu"

play_button = pygame.Rect(490, 390, 300, 70)
restart_button = pygame.Rect(490, 420, 300, 70)

def draw_text(text, font, color, x, y):
        image = font.render(text, True, color)
        rect = image.get_rect(center=(x, y))
        screen.blit(image, rect)

def draw_button(rect, text):
        mouse_pos = pygame.mouse.get_pos()

        if rect.collidepoint(mouse_pos):
            color = dark_orange
        else: 
            color = orange

        pygame.draw.rect(screen, color, rect, border_radius=14)
        draw_text(text, game_font, white, rect.centerx, rect.centery)

def reset_game():
      global dinosaur, game_speed, score, ground_x

      dinosaur_group.empty()
      obstacle_group.empty()
      cloud_group.empty()
      ptero_group.empty()

      dinosaur = dino.Dinosaur(50, 360)
      dinosaur_group.add(dinosaur)

      game_speed = 5
      score = 0
      ground_x = 0

#actual dino
dinosaur = dino.Dinosaur(50, 360)
dinosaur_group.add(dinosaur)

#spawns
spawn_obstacle = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_obstacle, 1500)

spawn_cloud = pygame.USEREVENT + 2
pygame.time.set_timer(spawn_cloud, 3000)

spawn_ptero = pygame.USEREVENT + 3
pygame.time.set_timer(spawn_ptero, 5000)

#main loop hayss
while True:
      dt = clock.tick(120) / 1000

      for event in pygame.event.get():

            if event.type == pygame.QUIT:
                  pygame.quit()
                  sys.exit()

            if event.type == pygame.KEYDOWN:

                if game_state in ("menu", "game_over"):
                        if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                              reset_game()
                              game_state = "playing"
                elif game_state == "playing":
                      if event.key in (pygame.K_SPACE, pygame.K_UP):
                            dinosaur.jump()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                if game_state == "menu":
                    if play_button.collidepoint(event.pos):
                        reset_game()
                        game_state = "playing"

                elif game_state == "game_over":
                    if restart_button.collidepoint(event.pos):
                        reset_game()
                        game_state = "playing"

            #objectspawns
            if game_state == "playing":

                if event.type == spawn_obstacle:
                        obstacle_group.add(obst.Obstacle())
                elif event.type == spawn_cloud:
                        cloud_group.add(clouds.Cloud())
                elif event.type == spawn_ptero:
                        ptero_group.add(obst.Ptero())

      if game_state == "playing":
            keys = pygame.key.get_pressed()

            if keys[pygame.K_DOWN]:
                  dinosaur.duck()
            elif dinosaur.is_ducking:
                  dinosaur.unduck()

            dinosaur_group.update()
            cloud_group.update()

            for obstacle in obstacle_group:
                obstacle.update(game_speed)

            for ptero in ptero_group:
                ptero.update(game_speed)

            score += dt * 10 #score directly proportional to survival time

            game_speed += 0.0015

            ground_x -= game_speed

            if ground_x <= -screen_width:
                  ground_x = 0

            hit_cactus = pygame.sprite.spritecollideany(
                  dinosaur, obstacle_group
            )

            hit_ptero = pygame.sprite.spritecollideany(
                  dinosaur, ptero_group
            )

            if hit_cactus or hit_ptero:
                  best_score = max(best_score, int(score))
                  game_state = "game_over"

      screen.fill(white)

      cloud_group.draw(screen)

      screen.blit(ground, (ground_x, ground_y))
      screen.blit(ground, (ground_x + screen_width, ground_y))

      dinosaur_group.draw(screen)
      obstacle_group.draw(screen)
      ptero_group.draw(screen)

      if game_state == "playing":
          draw_text(
                f"SCORE: {int(score):05d}",
                game_font, black, screen_width // 2, 475
          )

          draw_text(
                f"BEST: {best_score:05d}",
                small_font, gray, screen_width // 2, 515
          )
      if game_state == "menu":
            overlay = pygame.Surface(
                  (screen_width, screen_height), pygame.SRCALPHA
            )
            overlay.fill((255,255,255,190))
            screen.blit(overlay, (0,0))

            draw_text(
                  "darwin laptop",
                  title_font, black, screen_width // 2, 210
            )

            draw_text(
                  "runner laptop",
                  small_font, gray, screen_width // 2, 275
            )

            draw_button(play_button, "PLAY")

            draw_text(
                  "SPACE or UP for jump",
                  small_font, gray, screen_width // 2, 510
            )

            draw_text(
                  "DOWN to duck",
                  small_font, gray, screen_width // 2, 545
            )
      elif game_state == "game_over":
            overlay = pygame.Surface(
                  (screen_width, screen_height), pygame.SRCALPHA
            )
            overlay.fill((255, 255, 255, 200))
            screen.blit(overlay, (0, 0))

            draw_text(
                  "Game Over",
                  title_font, black, screen_width // 2, 220
            )

            draw_text(
                  f"SCORE {int(score)}",
                  game_font, black, screen_width // 2, 300
            )

            draw_text(
                  f"BEST: {best_score}",
                  game_font, gray, screen_width // 2, 345
            )

            draw_button(restart_button, "PLAY AGAIN")

            draw_text(
                  "press space/enter to restart",
                  small_font, gray, screen_width // 2, 530
            )
      pygame.display.update()
          
