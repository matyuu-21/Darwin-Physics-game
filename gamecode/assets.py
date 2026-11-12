import pygame
from asset_path import asset_path

_cache = {}

def load_image(path, size = None):
    key = (path, size)
    if key not in _cache:
        img = pygame.image.load(asset_path(path)).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
            _cache[key] = img
        return _cache[key]