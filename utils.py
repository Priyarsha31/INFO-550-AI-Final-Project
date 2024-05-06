import pygame
import sys
from settings import *

def load_and_slice_image(path, rows, cols):
    try:
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (300, 300))
        tile_width = image.get_width() // cols
        tile_height = image.get_height() // rows
        tiles = []
        for row in range(rows):
            for col in range(cols):
                rect = pygame.Rect(col * tile_width, row * tile_height, tile_width, tile_height)
                tile = image.subsurface(rect)
                tiles.append(tile)
        return tiles, tile_width, tile_height
    except pygame.error as e:
        print(f"Failed to load the image: {path}")
        raise SystemExit(e)

def draw_tiles(tile_order, tiles, tile_width, tile_height, window):
    for i, tile_idx in enumerate(tile_order):
        row = i // 3
        col = i % 3
        window.blit(tiles[tile_idx], (col * tile_width + (WINDOW_WIDTH - 300) // 2, row * tile_height + (WINDOW_HEIGHT - 300) // 2))