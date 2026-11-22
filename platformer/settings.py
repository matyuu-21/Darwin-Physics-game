import pygame

screen_width = 1280
screen_height = 900

fps = 60

tile = 64 #tile pixels

player_width = 52
player_height = 92

#movements per pixel per second
max_run = 380
ground_accel = 2600
ground_friction = 3000
air_accel = 1800
turn_boost = 1.5

jump_height_tiles = 3.5
time_to_apex = 0.40

#gravity 
earth_gravity = 2 * (jump_height_tiles * tile) / time_to_apex ** 2
jump_speed = earth_gravity * time_to_apex

fall_mult = 1.3 #multiplier
jump_cut = 0.45
max_fall = 1500 #max downward speed

coyote_time = 0.10 #jump time after a ledge
jump_buffer = 0.12 #remembering jump press

PLANETS = {
    "EARTH": 1,
    "MOON": 0.5,
    "JUPITER": 1.5
}

gravity_jump_mode = "same_speed"

camera_smooth = 8
camera_look_ahead = 100
camera_dead_zone = 80

coin_score = 10
stomp_score = 100
shot_kill_score = 50

max_lives = 3
invincible_time = 1.5

hit_knockback_x = 380
hit_knockback_y = -520

shoot_always = False
shoot_key = pygame.K_f
shot_speed = 720
shot_cooldown = 0.25
shot_lifetime = 1.2
max_shots = 3
shot_width = 24
shot_height = 12

checkpoint_color = (0, 200, 255)
checkpoint_width = 40
checkpoint_height = 64

#door stuff
goal_width = 48
goal_height = 80
goal_color = (40, 190, 100)
goal_frame_color = (25, 90, 55)
