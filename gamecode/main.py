import pygame, sys, random

import dino, obst, clouds, ui, powerup

pygame.init()

#screen variables
screen_width = 1280
screen_height = 720

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
pygame.display.set_caption("darwin laptop")
game_ui = ui.GameUI(screen)

#groups 
dinosaur_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()
cloud_group = pygame.sprite.Group()
ptero_group = pygame.sprite.Group()
powerup_group = pygame.sprite.Group()

#ground variables
ground = pygame.image.load("assets/ground.png")
ground = pygame.transform.scale(ground, (screen_width, 20))
ground_y = 360
ground_x = 0

game_speed = 5
score = 0 
best_score = 0
lives = 3
game_state = "menu"
has_shield = False
double_score_timer = 0.0

def reset_game():
      global dinosaur, game_speed, score, ground_x, lives, has_shield, double_score_timer

      dinosaur_group.empty()
      obstacle_group.empty()
      cloud_group.empty()
      ptero_group.empty()
      powerup_group.empty()

      dinosaur = dino.Dinosaur(50, 360)
      dinosaur_group.add(dinosaur)

      game_speed = 5
      score = 0
      lives = 3
      ground_x = 0
      has_shield = False
      double_score_timer = 0.0

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

spawn_powerup = pygame.USEREVENT + 4
pygame.time.set_timer(spawn_powerup, 8000)

#main loop hayss
while True:
      dt = clock.tick(60) / 1000

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
                    if game_ui.play_button.collidepoint(event.pos):
                        reset_game()
                        game_state = "playing"

                elif game_state == "game_over":
                    if game_ui.restart_button.collidepoint(event.pos):
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
                elif event.type == spawn_powerup:
                      if game_state == "playing":
                            powerup_group.add(powerup.PowerUp())

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

            for active_powerup in powerup_group:
                active_powerup.update(game_speed)  

            if double_score_timer > 0:
                  score += dt * 20
                  double_score_timer -= dt
            else:
                  score += dt * 10

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

            collected_powerup = pygame.sprite.spritecollideany(
                  dinosaur, powerup_group
            )

            if collected_powerup:
                  if collected_powerup.power_type == "heart":
                        lives = min(lives + 1, 3)
                  elif collected_powerup.power_type == "shield":
                        has_shield = True
                  elif collected_powerup.power_type == "double_score":
                        double_score_timer = 8.0

                  collected_powerup.kill()

            if hit_cactus or hit_ptero:
                  hit_obeject = hit_cactus if hit_cactus else hit_ptero
                  hit_obeject.kill()

                  if has_shield:
                        has_shield = False
                  else:
                        lives -= 1

            if lives <= 0:
                  lives = 0
                  best_score = max(best_score, int(score))
                  game_state = "game_over"

      screen.fill((255, 255, 255))

      cloud_group.draw(screen)

      screen.blit(ground, (ground_x, ground_y))
      screen.blit(ground, (ground_x + screen_width, ground_y))

      dinosaur_group.draw(screen)
      obstacle_group.draw(screen)
      ptero_group.draw(screen)
      powerup_group.draw(screen)

      if game_state == "playing":
            game_ui.draw_hud(score, best_score, lives)
      elif game_state == "menu":
            game_ui.draw_menu()
      elif game_state == "game_over":
            game_ui.draw_game_over(score, best_score)
      

      pygame.display.update()
          
