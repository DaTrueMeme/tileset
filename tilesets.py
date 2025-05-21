import os
import json
import math
from PIL import Image


class Tileset:
    def __init__(self, texture, tileset_json, temp_dir="tiles"):
        self.texture_path = texture
        self.tileset_path = tileset_json

        self.name = self.texture_path.split("/")[-1].split(".")[0]
        self.dir = f'{temp_dir}/{self.name}'

        with open(self.tileset_path, "r") as f:
            self.tileset_data = json.load(f)

        self.image = Image.open(texture)
        self.tile_size = self.tileset_data["tile_size"]

        self.width = self.tileset_data["width"]
        self.height = self.tileset_data["height"]

        if not os.path.exists(self.dir):
            self.generateImages()

    def generateImages(self):    
        os.mkdir(self.dir)

        texture_index = 0
        for y in range(self.height):
            for x in range(self.width):
                cropped_image = self.image.crop(
                    (
                        x * self.tile_size,
                        y * self.tile_size,
                        (x + 1) * self.tile_size,
                        (y + 1) * self.tile_size,
                    )
                )
                cropped_image.save(f"{self.dir}/{texture_index}.png")
                texture_index += 1

    def checkTile(self, tile, pos, world_tiles, world_size=None):
        width, height = world_size or (math.isqrt(len(world_tiles)),)*2
        def getTileAt(x, y):
            if 0 <= x < width and 0 <= y < height:
                return world_tiles[y * width + x]
            return "air"
        
        def matchesRule(real, rule):
            return all(rule[i] == real[i] or rule[i] == "3" for i in range(9))

        x, y = pos
    
        real = []
        for iy in range(3):
            for ix in range(3):
                rx = x + (ix - 1)
                ry = y + (iy - 1)
                real.append("1" if getTileAt(rx, ry) == tile else "0")
        real = ''.join(real)

        rules = self.tileset_data["ruleset"]
        tile = self.tileset_data["fallback"]
        for tile_index, rule in enumerate(rules):
            if matchesRule(real, rule):
                tile = tile_index
                break

        return f'{self.dir}/{tile}.png'