__author__ = 'craig'

import json
import pygame

class Loader():
    def __init__(self, map, screensize):
        f = open(map, "r")
        file_data = f.read()
        f.close()
        mapdict = json.loads(file_data)

        self.height = mapdict["height"]
        self.tileheight = mapdict["tileheight"]
        self.tilesets = mapdict["tilesets"]
        self.width = mapdict["width"]
        self.tilewidth = mapdict ["tilewidth"]
        self.layers = mapdict["layers"]
        self.screenwidth = screensize[0]
        self.screenheight = screensize[1]
        #self.mapwidth = self.width * self.tilewidth
        #self.mapheight = self.height * self.tileheight

    def load_tiles(self):
        all_tiles = []

        for tileset in self.tilesets:
            image = tileset["image"]
            imageheight = tileset["imageheight"]
            imagewidth = tileset["imagewidth"]
            tileheight = tileset["tileheight"]
            tilewidth = tileset["tilewidth"]
            tileset_surface = pygame.image.load(image)
            for y in range (0, imageheight, tileheight):
                for x in range (0, imagewidth, tilewidth):
                    tile = pygame.Surface((tilewidth, tileheight))
                    tile.blit(tileset_surface, (0,0), (x, y, tilewidth, tileheight))
                    all_tiles.append(tile)
        return(all_tiles)

    def load_layers(self):
        all_layers = []
        collide_rects =[]
        all_tiles = self.load_tiles()
        for layer in self.layers:
            #layer = self.layers[0]
            collide = "0"
            data_index = 0
            data = layer["data"]
            height  = layer["height"]
            width = layer["width"]
            properties = layer["properties"]
            collide = properties.get("collision")
            if collide == "1":
                print("this layer has collision")
            elif collide == "0":
                print ("this layer has no collision")
            self.surface_width = self.tilewidth * width
            self.surface_height = self.tileheight * height
            surface = pygame.Surface((self.surface_width, self.surface_height))
            for y in range (0, self.surface_height, self.tileheight):
                for x in range (0, self.surface_width, self.tilewidth):
                    tile_id = data[data_index]
                    if tile_id > 0:
                        tile_index = tile_id -1
                        tile = all_tiles[tile_index]
                        surface.blit(tile, (x, y))
                        if collide == "1":
                            newtile = pygame.Rect(x, y, self.tilewidth, self.tileheight)
                            # shrink tile to make collision more forgiving
                            smalltile = newtile.inflate(-16, -16)
                            # smalltile.center = newtile.center
                            collide_rects.append(smalltile)
                    data_index += 1

            surface.set_colorkey((0,0,0))
            all_layers.append(surface)
        return (all_layers, collide_rects)

    def move_map(self, direction, rect, collide_rects):
        speed = 2
        if direction == "right":
            rect.right -= speed
        elif direction == "left":
            rect.left += speed
        elif direction == "up":
            rect.top += speed
        elif direction == "down":
            rect.bottom -= speed
        for collidetile in collide_rects:
            if direction == "right":
                collidetile.right -= speed
            elif direction == "left":
                collidetile.left += speed
            elif direction == "up":
                collidetile.top += speed
            elif direction == "down":
                collidetile.bottom -= speed
        return (rect, collide_rects)

    def initialize_map(self, offset, rect, collide_rects):
        rect.bottom = rect.bottom + offset[1]
        rect.left = rect.left + offset[0]
        for collidetile in collide_rects:
            collidetile.bottom += offset[1]
            collidetile.left += offset[0]
        return(rect, collide_rects)


    def check_boundary(self, rect):
        self.hit_boundary = None
        if (rect.left >= 0):
            self.hit_boundary = "left"
            print("hit left boundary")
        elif (rect.right) <= self.screenwidth:
            print("hit right boundary")
            self.hit_boundary = "right"
        elif rect.top >= 0:
            print("hit top")
            self.hit_boundary = "up"
        elif rect.bottom <= self.screenheight:
            print ("hit bottom")
            self.hit_boundary = "down"
        return (self.hit_boundary)

    def handle_boundary(self, direction):
        if self.hit_boundary == "left":
            direction = "right"
        elif self.hit_boundary == "right":
            direction = "left"
        elif self.hit_boundary == "up":
            direction = "down"
        elif self.hit_boundary == "down":
            direction = "up"

        return(direction)
