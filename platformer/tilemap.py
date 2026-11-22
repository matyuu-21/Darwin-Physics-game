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

        self.reserved_tiles = "CE^|BGK?" #for future phases

        self.spawns = []
        self.hazard_rects = []

    def load(self, path):
        path = Path(path)
        text = path.read_text(encoding="utf-8")

        rows = [line.rstrip("\r") for line in text.splitlines() if line.strip()]

        if not rows:
            raise ValueError("The level file is empty")

        self.width = max(len(row) for row in rows)
        self.height = len(rows)

        self.tiles = [list(row.ljust(self.width, ".")) for row in rows]

        self.width_px = self.width * settings.tile
        self.height_px = self.height * settings.tile

        self.spawns = []
        self.hazard_rects = []

        #player spawn n checking unkown char
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

                elif tile not in "#." + self.reserved_tiles:
                    print(f"warning: unknown tile char '{tile}'. it is empty.")

        if not spawn_found:
            print("warning no p spawn found, use default")

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
                    pygame.draw.rect(
                        screen,
                        (145, 95, 55),
                        camera.apply(tile_rect)
                    )

                    pygame.draw.rect(
                        screen,
                        (85, 50, 30),
                        camera.apply(tile_rect),
                        2
                    )
        self.draw_hazards(screen, camera)

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