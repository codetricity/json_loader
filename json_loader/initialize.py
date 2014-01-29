__author__ = 'craig'

import pygame
import json
from player import *
from map import *


class Initialize():
    def __init__(self, phone_screen, testing, filename, player_image_file):
        try:
            with open(filename) as mapfile:
                self.mapdict = json.loads(mapfile.read())
                self.layers = self.mapdict["layers"]
                self.mapheight = self.layers[0]["height"] * 32
                self.mapwidth = self.layers[0]["width"] * 32
        except IOError:
            print("Cannot open map file {}".format(filename))

        self.test = testing
        self.phone_rect = phone_screen.get_rect()
        self.test_button = pygame.Rect(5, 5, 20, 100)

        self.player = Player(self.phone_rect.center, player_image_file)
        self.tileset()
        self.build()

    def build(self):
        self.all_layers = []
        self.collision_layers = []

        collision_tinted_surface = pygame.Surface((32, 32))
        collision_tinted_surface.fill((255, 0, 0))
        collision_tinted_surface.set_alpha(30)

        for layer in self.layers:
            current_layer = []
            collision_flag = False
            if "properties" in layer:
                properties = layer["properties"]
                if "collision" in properties:
                    if properties["collision"] == "1":
                        collision_flag = True
                        current_collision_layer = []
            data = layer["data"]
            index = 0
            for y in range(0, layer["height"]):
                for x in range(0, layer["width"]):
                    id_key = data[index]
                    if id_key != 0:
                        tile = Tile()
                        tile.rect = pygame.Rect(x * 32, y * 32, 32, 32)
                        tile.image = self.all_tiles[id_key]
                        current_layer.append(tile)
                        if collision_flag:
                            collision_tile = Tile()
                            collision_tile.image = collision_tinted_surface
                            collision_tile.rect = tile.rect.copy()
                            current_collision_layer.append(collision_tile)
                    index += 1
            self.all_layers.append(current_layer)
            if collision_flag:
                self.collision_layers.append(current_collision_layer)

        return self.all_layers, self.collision_layers

    def tileset(self):
        tilesets = self.mapdict["tilesets"]
        tile_id = 1
        self.all_tiles = {}

        for tileset in tilesets:
            tilesurface = pygame.image.load("maps/" + tileset["image"]).convert_alpha()
            for y in range(0, tileset["imageheight"], 32):
                for x in range(0, tileset["imagewidth"], 32):
                    rect = pygame.Rect(x, y, 32, 32)
                    tile = tilesurface.subsurface(rect)
                    self.all_tiles[tile_id] = tile
                    tile_id += 1
        return self.all_tiles
