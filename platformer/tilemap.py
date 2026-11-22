from pathlib import Path
import pygame, settings

class Tilemap:
    def __init__(self):
        self.tiles = []
        self.width = 0
        self.height = 0

        self.width_px = 0
        self.height_px = 0

        self.spawn_point = (settings.tile, settings.tile)

        self.reserved_tiles = "CE^|GK?" 

        self.spawns = []
        self.hazard_rects = []
        self.checkpoint_rects = []
        self.goal_rects = []

        self.boss_room_col = None
        self.boss_room_left = None
        self.boss_spawn = None

        self.gate_original_column = None
        self.gate_closed = False

        self.boss_room_cleared = False

    def load(self, path):
        self.checkpoint_rects = []

        path = Path(path)
        text = path.read_text(encoding="utf-8")

        rows = [line.rstrip("\r") for line in text.splitlines() if line.strip()]

        if not rows:
            raise ValueError("level file empty")

        self.width = max(len(row) for row in rows)
        self.height = len(rows)

        self.tiles = [list(row.ljust(self.width, ".")) for row in rows]

        self.width_px = self.width * settings.tile
        self.height_px = self.height * settings.tile

        self.spawns = []
        self.hazard_rects = []
        self.goal_rects = []
        self.checkpoint_rects = []

        self.boss_room_col = None
        self.boss_room_left = None
        self.boss_spawn = None

        self.gate_original_column = None
        self.gate_closed = False
        self.boss_room_cleared = False

        spawn_found = False

        for row in range(self.height):
            for col in range(self.width):
                tile = self.tiles[row][col]

                if tile == "P":
                    spawn_x = col * settings.tile
                    spawn_y = (row + 1) * settings.tile - settings.player_height

                    self.spawn_point = (float(spawn_x), float(spawn_y))

                    self.tiles[row][col] = "."
                    spawn_found = True

                elif tile == "C":
                    self.spawns.append(("C", col, row))
                    self.tiles[row][col] = "."

                elif tile == "^":
                    spike_rect = pygame.Rect(
                        col * settings.tile + 8,
                        row * settings.tile + settings.tile // 2,
                        settings.tile - 16,
                        settings.tile // 2
                    )   

                    self.hazard_rects.append(spike_rect)
                    self.tiles[row][col] = "."

                elif tile == "K":
                    checkpoint_rect = pygame.Rect(
                        col * settings.tile
                        + (settings.tile - settings.checkpoint_width) // 2,
                        row * settings.tile
                        + settings.tile
                        - settings.checkpoint_height,
                        settings.checkpoint_width,
                        settings.checkpoint_height
                    )

                    self.checkpoint_rects.append(self.checkpoint_rects)
                    self.tiles[row][col] = "."

                elif tile == "G":
                    goal_rect = pygame.Rect(
                        col * settings.tile
                        + (settings.tile - settings.goal_width) // 2,
                        (row + 1) * settings.tile - settings.goal_height,
                        settings.goal_width,
                        settings.goal_height
                    )

                    self.goal_rects.append(goal_rect)
                    self.tiles[row][col] = "."

                elif tile == "B":
                    if self.boss_room_col is not None:
                        print("warning: more than one boss marker found")
                    else:
                        self.boss_room_col = col
                        self.boss_room_left = col * settings.tile

                    self.tiles[row][col] = "."

                elif tile == "X":
                    if self.boss_spawn is not None:
                        print("warning: more than one boss marker found")
                    else:
                        spawn_x = col * settings.tile + settings.tile / 2
                        spawn_y = (row + 1) * settings.tile

                        self.boss_spawn = (float(spawn_x), float(spawn_y))

                    self.tiles[row][col] = "."

                elif tile not in "#" + self.reserved_tiles:
                    print("unknown tile")

        if not spawn_found:
            print("no p spawn found, use default")

        if self.boss_room_col is not None:
            expected_width = (
                self.boss_room_col + settings.boss_room_columns
            )

            if self.width != expected_width:
                print("boss room must end at level's right edge")

    def close_gate(self):
        if self.boss_room_col is None:
            return

        if self.gate_closed:
            return

        self.gate_original_column = []

        for row in range(self.height):
            original_tile = self.tile[row][self.boss_room_col]
            self.gate_original_column.append(original_tile)

            self.tiles[row][self.boss_room_col] = "#"

        self.gate_closed = True

    def open_gate(self):
        if not self.gate_closed:
            return

        for row in range(self.height):
            self.tiles[row][self.boss_room_col] = (
                self.gate_original_column[row]
            )

        self.gate_original_column = None
        self.gate_closed = False

    def is_goal_locked(self, goal_rect):
        if self.boss_room_left is None:
            return False

        goal_is_inside_room = goal_rect.centerx >= self.boss_room_left
        return goal_is_inside_room and not self.boss_room_cleared


    def is_solid(self, col, row):
        if col < 0 or col >= self.width:
            return True

        if row >= self.height:
            return False

        if row < 0:
            return False

        return self.tiles[row][col] == "#"

    def get_solid_tiles(self, rect):
        tile_size = settings.tile

        left = rect.left // tile_size 
        right = (rect.right - 1) // tile_size
        top = rect.top // tile_size
        bottom = (rect.bottom - 1) // tile_size

        solid_tiles = []

        for row in range(top, bottom + 1):
            for col in range(left, right + 1):
                if self.is_solid(col, row):
                    tile_rect = pygame.Rect(
                        col * tile_size,
                        row * tile_size,
                        tile_size,
                        tile_size
                    )
                    solid_tiles.append(tile_rect)

        return solid_tiles

    def draw(self, screen, camera):
        tile_size = settings.tile

        camera_x = camera.x
        camera_y = camera.y

        start_col = max(0, int(camera_x // tile_size))
        end_col = min(
            self.width,
            int((camera_x + screen.get_width()) // tile_size) + 1
        )

        start_row = max(0, int(camera_y // tile_size))
        end_row = min(
            self.height,
            int((camera_y + screen.get_height()) // tile_size) + 1
        )

        for row in range(start_row, end_row):
            for col in range(start_col, end_col):

                if self.tiles[row][col] == "#":

                    tile_rect = pygame.Rect(
                        col * tile_size,
                        row * tile_size,
                        tile_size,
                        tile_size
                )

                #brown tile
                    if self.gate_closed and col == self.boss_room_col:
                        tile_color = settings.boss_gate_colo
                        frame_color = (60, 15, 25)
                    else:
                        tile_color = (145, 95, 55)
                        frame_color = (85, 50, 30)

                    pygame.draw.rect(
                        screen, tile_color, camera.apply(tile_rect)
                    )

                    pygame.draw.rect(
                        screen, frame_color, camera.apply(tile_rect), 2
                    )
        self.draw_hazards(screen, camera)
        self.draw_goals(screen, camera)

    def draw_hazards(self, screen, camera):
        for hazard_rect in self.hazard_rects:

            screen_rect = camera.apply(hazard_rect)

            points = [
                (screen_rect.centerx, screen_rect.top),
                (screen_rect.right, screen_rect.bottom),
                (screen_rect.left, screen_rect.bottom)
            ]

            pygame.draw.polygon(
                screen,
                (150, 150, 150),
                points
            )

            pygame.draw.polygon(
                screen,
                (70, 70, 70),
                points, 2
            )

    def draw_goals(self, screen, camera):
        for goal_rect in self.goal_rects:
            screen_rect = camera.apply(goal_rect)

            if self.is_goal_locked(goal_rect):
                # Locked goals are gray
                door_color = (100, 100, 100)
                frame_color = (55, 55, 55)
                light_color = (160, 160, 160)
            else:
                door_color = settings.goal_color
                frame_color = settings.goal_frame_color
                light_color = (255, 230, 100)

            pygame.draw.rect(
                screen,
                door_color,
                screen_rect
            )

            pygame.draw.rect(
                screen,
                frame_color,
                screen_rect,
                4
            )

            pygame.draw.circle(
                screen,
                light_color,
                (screen_rect.right - 10, screen_rect.centery),
                4
            )