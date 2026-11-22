import pygame
from entities import Coin

class CoinManager:
    def __init__(self, tilemap):
        self.coins = []

        for spawn in tilemap.spawns:
            tile_type, col, row = spawn

            if tile_type == "C":
                self.coins.append(Coin(col, row))

    def update(self, dt):
        for coin in self.coins:
            if not coin.collected:
                coin.update(dt)

    def collect(self, player):
        collected = 0

        for coin in self.coins:
            if (
                not coin.collected
                and player.rect.colliderect(coin.rect)
            ):
                coin.collected = True
                collected += 1
        return collected

    def draw(self, screen, camera):
        for coin in self.coins:
            if not coin.collected:
                coin.draw(screen, camera)
