import pygame
import random
from tilesets import Tileset

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

class Camera:
    def __init__(self, x, y):
        self.x, self.y = x, y
    
    def move(self, speed=3):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= speed
        if keys[pygame.K_RIGHT]:
            self.x += speed
        if keys[pygame.K_UP]:
            self.y -= speed
        if keys[pygame.K_DOWN]:
            self.y += speed
camera = Camera(0, 0)

class Tile:
    def __init__(self, tile, x, y):
        self.tile = tile
        self.x, self.y = x, y

        self.texture = None

    def setTile(self, path):
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (tile_size, tile_size))

    def render(self):
        if self.texture is not None:
            screen.blit(self.texture, (self.x - camera.x, self.y - camera.y))

world_size = 50
tile_size = 32
world = []
for y in range(world_size):
    for x in range(world_size):
        tiles = ["red", "blue", "green"]
        tile = random.choice(tiles)
        
        world.append(Tile(tile, x * tile_size, y * tile_size))

world_tiles = []
for tile in world:
    world_tiles.append(tile.tile)
    
red_tileset = Tileset("red_rocks.png", "tilesets/5x4.json")
blue_tileset = Tileset("blue_rocks.png", "tilesets/5x4.json")
green_tileset = Tileset("green_rocks.png", "tilesets/5x4.json")
for tile in world:
    if tile.tile != "air":
        x, y = tile.x // tile_size, tile.y // tile_size
        if tile.tile == "red":
            texture_path = red_tileset.checkTile(tile.tile, (x, y), world_tiles)
        elif tile.tile == "blue":
            texture_path = blue_tileset.checkTile(tile.tile, (x, y), world_tiles)
        else:
            texture_path = green_tileset.checkTile(tile.tile, (x, y), world_tiles)

        tile.setTile(texture_path)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("black")

    camera.move(8)
    for tile in world:
        tile.render()

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
