import pygame, sys, random, os

import dino, obst, clouds, ui, powerup, buildings, boss, projectile
from asset_path import asset_path
from stage_manager import StageManager

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
building_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()
projectile_group = pygame.sprite.Group()

#stage manager variable
stage_manager = StageManager()

#ground variables & background
ground = pygame.image.load(asset_path("assets/ground.png"))
ground = pygame.transform.scale(ground, (screen_width, 20))
ground_y = 460
other_y = 480
ground_x = 0

def load_stage_background():
      current_stage = stage_manager.get_current_stage()
      raw = pygame.image.load(asset_path(current_stage["background"])).convert()
      raw = pygame.transform.scale(raw, (screen_width, screen_height))
      raw.set_alpha(150)
      baked = pygame.Surface((screen_width, screen_height))
      baked.fill((255, 255, 255))
      baked.blit(raw, (0, 0))
      return baked.convert()

background_sky = load_stage_background()

background_sky_level = 0
background_sky_x = 0
background_sky_speed = 1
building_speed = 1
building_gap = 500

game_speed = 5
score = 0 
best_score = 0
lives = 3
game_state = "menu"
has_shield = False
rainbow_timer = 0
rainbow_duration = 15
rainbow_speed = 1.5
double_score_timer = 0.0

def reset_game():
      global dinosaur, game_speed, score, ground_x, background_x, lives, has_shield, double_score_timer, background_sky_x, building_gap, building_speed, boss_defeated, rainbow_timer, background_sky

      dinosaur_group.empty()
      obstacle_group.empty()
      cloud_group.empty()
      ptero_group.empty()
      powerup_group.empty()
      building_group.empty()
      boss_group.empty()
      projectile_group.empty()

      dinosaur = dino.Dinosaur(50, other_y)
      dinosaur_group.add(dinosaur)

      game_speed = 5
      score = 0
      lives = 3
      ground_x = 0
      has_shield = False
      double_score_timer = 0.0
      rainbow_timer = 0
      building_speed = 1
      building_gap = 500
      background_sky_x = 0 
      stage_manager.reset()
      background_sky = load_stage_background()
      restart_spawn_timers()


#actual dino
dinosaur = dino.Dinosaur(50, other_y)
dinosaur_group.add(dinosaur)

#spawns
spawn_obstacle = pygame.USEREVENT + 1
spawn_cloud = pygame.USEREVENT + 2
spawn_ptero = pygame.USEREVENT + 3
spawn_powerup = pygame.USEREVENT + 4

SPAWN_INTERVALS = {
      spawn_obstacle: 1500,
      spawn_cloud: 3000,
      spawn_ptero: 5000,
      spawn_powerup: 8000
}

def restart_spawn_timers():
      for event_id, ms in SPAWN_INTERVALS.items():
            pygame.time.set_timer(event_id, ms)
restart_spawn_timers()

MIN_GAP = 350

def spawn_lane_clear():
      return all(
            s.rect.right < screen_width - MIN_GAP
            for g in (obstacle_group, ptero_group)
            for s in g
      )

SHOT_DELAY = 0.25
shot_cooldown = 0

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

                  elif game_state == "boss_fight":
                        if event.key in (pygame.K_SPACE, pygame.K_UP):
                              dinosaur.jump()
                        elif event.key == pygame.K_f and boss_group and shot_cooldown <= 0:
                              shot_cooldown = SHOT_DELAY
                              shot = projectile.Projectile(
                                    dinosaur.rect.right,
                                    dinosaur.rect.centery
                              )
                              projectile_group.add(shot)
                  elif game_state == "victory":
                        if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                              reset_game()
                              game_state = "playing"

            if event.type == pygame.KEYUP:
                  if event.key in (pygame.K_SPACE, pygame.K_UP):
                        dinosaur.release_jump()    


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

                if event.type == spawn_obstacle and spawn_lane_clear():
                        obstacle_group.add(obst.Obstacle())
                elif event.type == spawn_cloud:
                        cloud_group.add(clouds.Cloud())
                elif event.type == spawn_ptero and spawn_lane_clear():
                        ptero_group.add(obst.Ptero())
                elif event.type == spawn_powerup:
                      if game_state == "playing":
                            powerup_group.add(powerup.PowerUp())

      if game_state in ("playing", "boss_fight"):

            if rainbow_timer > 0:
                  rainbow_timer -= dt

            if rainbow_timer < 0:
                  rainbow_timer = 0

            dinosaur.is_rainbow = rainbow_timer > 0

      if game_state == "playing":
            keys = pygame.key.get_pressed()

            if keys[pygame.K_DOWN]:
                  dinosaur.duck()
            elif dinosaur.is_ducking:
                  dinosaur.unduck()

            current_speed = game_speed

            if rainbow_timer > 0:
                  current_speed *= rainbow_speed

            dinosaur_group.update(dt)
            cloud_group.update()
            building_group.update(building_speed)

            #if len(building_group) == 0:
                  #uilding_group.add(buildings.Building())
           # else:
                  #rightmost_building = max(
                      #  building_group, key=lambda building: building.rect.right #fix this soon after boss i guess
                  #)

                  #if rightmost_building.rect.right <= screen_width - building_gap:
                       # building_group.add(buildings.Building())
                       # building_gap = random.randint(250, 500)

            for obstacle in obstacle_group:
                obstacle.update(current_speed)

            for ptero in ptero_group:
                ptero.update(current_speed)

            for active_powerup in powerup_group:
                active_powerup.update(current_speed)  

            if double_score_timer > 0:
                  score += dt * 20
                  double_score_timer -= dt
            else:
                  score += dt * 10

            game_speed += 0.0015

            #background_sky_x -= background_sky_speed
            #if background_sky_x <= -screen_width:
                  #background_sky_x += screen_width

            ground_x -= current_speed

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
                  elif collected_powerup.power_type == "super_jump":
                        dinosaur.jump_strength = -45
                        dinosaur.jump_timer = 8
                  elif collected_powerup.power_type == "rainbow_star":
                        rainbow_timer = rainbow_duration
                        dinosaur.is_rainbow = True

                  collected_powerup.kill()

            dino_hitbox = dinosaur.get_hitbox()

            hit_cactus = None
            hit_ptero = None
            for obstacle in obstacle_group:
                  if dino_hitbox.colliderect(obstacle.rect):
                        hit_cactus = obstacle
                        break
            for ptero in ptero_group:
                  ptero_hitbox = ptero.rect.inflate(-10, -10)

                  if dino_hitbox.colliderect(ptero_hitbox):
                        hit_ptero = ptero
                        break

            if hit_cactus or hit_ptero:
                  hit_object = hit_cactus if hit_cactus else hit_ptero
                  hit_object.kill()

                  if not dinosaur.is_rainbow:
                        if has_shield:
                              has_shield = False
                        else:
                              lives -= 1

            if lives <= 0:
                  lives = 0
                  best_score = max(best_score, int(score))
                  game_state = "game_over"

            if stage_manager.check_boss_trigger(score):

                  current_stage = stage_manager.get_current_stage()
                  obstacle_group.empty()
                  ptero_group.empty()
                  powerup_group.empty()

                  boss_group.add(boss.Boss(1000, 350, current_stage))
                  game_state = "boss_fight"

      if game_state == "boss_fight":
            
            shot_cooldown = max(0, shot_cooldown - dt)
            keys = pygame.key.get_pressed()

            if keys[pygame.K_DOWN]:
                  dinosaur.duck()
            elif dinosaur.is_ducking:
                  dinosaur.unduck()

            dinosaur_group.update(dt)
            boss_group.update(dt)    
            projectile_group.update()

            for shot in list(projectile_group):
                  hits = pygame.sprite.spritecollide(
                        shot, boss_group, False
                  )

                  if hits:
                        hits[0].damage(shot.damage)
                        shot.kill()
      if game_state == "boss_fight" and boss_group:
            current_boss = boss_group.sprites()[0]

            if current_boss.state == "dashing":
                  dino_hitbox = dinosaur.get_hitbox()
                  boss_hitbox = current_boss.rect.inflate(-30, -30)

                  if dino_hitbox.colliderect(boss_hitbox):
                        if not dinosaur.is_rainbow:
                              if has_shield:
                                    has_shield = False
                              else:
                                    lives -= 1

                        current_boss.state = "recovering"
                        current_boss.image = current_boss.original_image
                        current_boss.rect = current_boss.image.get_rect(
                              center=current_boss.rect.center
                        )
      if lives <= 0:
            lives = 0
            best_score = max(best_score, int(score))
                  
            boss_group.empty()
            projectile_group.empty()

            game_state = "game_over"

      elif game_state == "boss_fight" and not boss_group:
            projectile_group.empty()

            result = stage_manager.complete_boss()

            if result == "next_stage":
                  current_stage = stage_manager.get_current_stage()
                  background_sky = load_stage_background()
                  restart_spawn_timers()
                  game_state = "playing"
            elif result == "game_complete":
                  best_score = max(best_score, int(score))
                  game_state = "victory"
#DRAWING 
      #screen.fill((255, 255, 255))

      #screen.blit(background_sky, (background_sky_x, background_sky_level))
      #screen.blit(background_sky, (background_sky_x + screen_width, background_sky_level))
 #transparency
      screen.blit(background_sky, (0,0))

      #building_group.draw(screen)
      #cloud_group.draw(screen)

      screen.blit(ground, (ground_x, ground_y))
      screen.blit(ground, (ground_x + screen_width, ground_y))

      dinosaur_group.draw(screen)
      obstacle_group.draw(screen)
      ptero_group.draw(screen)
      powerup_group.draw(screen)
      boss_group.draw(screen)
      projectile_group.draw(screen)

      if game_state == "boss_fight" and boss_group:
            boss_enemy = next(iter(boss_group))
            boss_enemy.health_bar(screen)

      if game_state == "playing":
            game_ui.draw_hud(score, best_score, lives)
      elif game_state == "menu":
            game_ui.draw_menu()
      elif game_state == "game_over":
            game_ui.draw_game_over(score, best_score)
      elif game_state == "boss_fight":
            game_ui.draw_hud(score, best_score, lives)
      elif game_state == "victory":
            screen.fill((20, 25, 45))

            victory_font = pygame.font.Font(None, 90)
            message = victory_font.render("YOU WIN", True, (255, 215, 0))

            message_rect = message.get_rect(
                  center=(screen_width // 2, screen_height // 2)
            )

            screen.blit(message, message_rect)
            hint = game_ui.small_font.render(
                  "press space/enter to play again", True, (200, 200, 210))
            screen.blit(hint, hint.get_rect(
                  center=(screen_width // 2, screen_height // 2 + 70)
            ))

      pygame.display.update()
          