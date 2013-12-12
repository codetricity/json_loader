"""
View README.md for more information.

Steps to build a 2D tile map loader
---------------------------------
1. Mapfile

    Example: class Initialize

    1.1 read json map file from disk

    1.2 load into python dictionary


2. Tilesets

    Example: class Intialize.tileset()

    2.1 extract list of tilesets from map dictionary


    2.2 for each tileset, slice a 32x32 pixel square

    2.3 load each tile into a dictionary of all tiles from all the tilesets

3. Display Tiles

    Example: Initialize.build()

4. Display Player

    Example: class Player

5. Check for touchscreen input and set direction (or keyboard on desktop computer)

    Example: class Event()

    5.1 Keyboard input using arrow keys


    5.2 touchscreen input

        - create virtual game controller

        Example: class GameController()

        - check for touchscreen input with virtual game controller

        Example: Event.mouse_direction()

6. Move Tiles

    Example: class Map.update(direction) and class Map.move(x = 0, y = 0)

7. Check boundaries

    Example: Map.clear_to_move()

8. Handle collision

    Example: Layer.check_collision()
"""



__author__ = 'craig'
import json
# you need Pygame http://pygame.org and Python 2.7 to run these
# examples
import pygame, sys

# code specific to running games on Android
try:
    import android
except ImportError:
    android = None
if android:
    android.init()
    android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)


class Player(pygame.sprite.Sprite):
    def __init__(self, center, filename):
        pygame.sprite.Sprite.__init__(self)

        try:
            self.image = pygame.image.load(filename).convert_alpha()
        except IOError:
            print("Cannot find player file {}".format(filename))
        self.rect = self.image.get_rect()
        self.rect.center = center

class Tile(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Map():
    def __init__(self, initial):
        self.initial = initial
        self.all_layers = initial.all_layers
        self.collision_layers = initial.collision_layers
        self.mapheight = initial.mapheight
        self.mapwidth = initial.mapwidth
        self.speed = 3

        topleft = self.all_layers[0][0].rect.topleft
        self.mapx = topleft[0]
        self.mapy = topleft[1]
        self.player = initial.player
        self.phone_width = initial.phone_rect.width
        self.phone_height = initial. phone_rect.height
        self.virtual_game_controller = GameController(initial)


    def check_collision(self):
        adjust = [0, 0]
        if self.direction == "left":
            adjust = [self.speed, 0]
        elif self.direction == "right":
            adjust = [0- self.speed, 0]
        elif self.direction == "up":
            adjust = [0, self.speed]
        elif self.direction == "down":
            adjust = [0, 0 - self.speed]
        for collision_layer in self.collision_layers:
            tmp_list = []
            tmp_list.extend(collision_layer)
            for tile in tmp_list:
                tmp_rect = tile.rect.move(adjust)
                if tmp_rect.colliderect(self.player.rect):
                    self.clear_move = False


    def clear_to_move(self):
        self.clear_move = True

        if self.direction == "left" and self.mapx + self.speed > 0:
            self.clear_move = False
        if self.direction == "right" and self.mapx < self.phone_width - self.mapwidth - self.speed:
            self.clear_move = False
        if self.direction == "up" and self.mapy + self.speed > 0:
            self.clear_move = False
        if self.direction == "down" and self.mapy < self.phone_height - self.mapheight + self.speed:
            self.clear_move = False

        if self.clear_move:
            self.check_collision()
        return (self.clear_move)



    def update(self, direction):
        x = 0
        y = 0
        self.direction = direction
        if self.clear_to_move():
            if direction == "right":
                x -= self.speed
            elif direction == "left":
                x += self.speed
            elif direction == "up":
                y += self.speed
            elif direction == "down":
                y -= self.speed
        self.move(x, y)


    def move(self, x = 0, y = 0):
        self.mapx += x
        self.mapy += y
        for current_layer in self.all_layers:
            for tile in current_layer:
                tile.rect.move_ip(x, y)
        for collision_layer in self.collision_layers:
            for tile in collision_layer:
                tile.rect.move_ip(x,y)

    def display(self, screen):
        for layer in self.all_layers:
            for tile in layer:
                screen.blit(tile.image, tile.rect)
        if self.initial.test:
            for layer in self.collision_layers:
                for collision_tile in layer:
                    screen.blit(collision_tile.image, collision_tile.rect)

            screen.blit(self.virtual_game_controller.leftbutton,
                            self.virtual_game_controller.left)
            screen.blit(self.virtual_game_controller.rightbutton,
                            self.virtual_game_controller.right)
            screen.blit(self.virtual_game_controller.upbutton,
                            self.virtual_game_controller.up)
            screen.blit(self.virtual_game_controller.downbutton,
                            self.virtual_game_controller.down)



            

        screen.blit(self.player.image, self.player.rect)

class Event():
    def __init__(self, initial):
        self.direction = "stop"
        self.virtual_game_controller = GameController(initial)

    def update(self):
        # check for android pause event
        if android:
            if android.check_pause():
                android.wait_for_resume()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.direction = "up"
                elif event.key == pygame.K_DOWN:
                    self.direction = "down"
                elif event.key == pygame.K_LEFT:
                    self.direction = "left"
                elif event.key == pygame.K_RIGHT:
                    self.direction = "right"

        self.mouse_direction()

    def mouse_direction(self):
        """
        Sets direction based on touchscreen input.
        Checks for mouse position (same as touchscreen)
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.virtual_game_controller.left.collidepoint(mouse_pos):
            self.direction = "left"
        elif self.virtual_game_controller.right.collidepoint(mouse_pos):
            self.direction = "right"
        if self.virtual_game_controller.up.collidepoint(mouse_pos):
            self.direction = "up"
        elif self.virtual_game_controller.down.collidepoint(mouse_pos):
            self.direction = "down"


class Initialize():

    def __init__(self, phone_screen, testing, filename,  player_image_file):
        try:
            mapfile = open(filename)
        except IOError:
            print("Cannot open map file {}".format(filename))
        jsondata = mapfile.read()
        self.test = testing
        self.mapdict = json.loads(jsondata)
        self.layers = self.mapdict["layers"]
        self.mapheight = self.layers[0]["height"] * 32
        self.mapwidth = self.layers[0]["width"] * 32
        self.phone_rect = phone_screen.get_rect()

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
            if layer.has_key("properties"):
                properties = layer["properties"]
                if properties.has_key("collision"):
                    if properties["collision"] == "1":
                        collision_flag = True
                        current_collision_layer = []
            data = layer["data"]
            index = 0
            for y in range(0, layer["height"]):
                for x in range (0, layer["width"]):
                    id_key = data[index]
                    if id_key != 0:
                        tile = Tile()
                        tile.rect = pygame.Rect(x * 32, y * 32, 32, 32)
                        tile.image = self.all_tiles[id_key]
                        current_layer.append(tile)
                        if collision_flag == True:
                            collision_tile = Tile()
                            collision_tile.image = collision_tinted_surface
                            collision_tile.rect = tile.rect.copy()
                            current_collision_layer.append(collision_tile)
                    index += 1
            self.all_layers.append(current_layer)
            if collision_flag == True:
                self.collision_layers.append(current_collision_layer)

        return (self.all_layers, self.collision_layers)


    def tileset(self):

        tilesets = self.mapdict["tilesets"]


        tile_id = 1
        self.all_tiles = {}

        for tileset in tilesets:
            tilesurface = pygame.image.load(tileset["image"]).convert_alpha()
            for y in range(0, tileset["imageheight"], 32):
                for x in range (0, tileset["imagewidth"], 32):
                    rect = pygame.Rect(x, y, 32, 32)
                    tile = tilesurface.subsurface(rect)
                    self.all_tiles[tile_id] = tile
                    tile_id += 1
        return(self.all_tiles)

class GameController():
    def __init__(self, initial):

        #adjust the size of the controller button.
        size = 100
        screen = initial.phone_rect.copy()
        self.left = pygame.Rect(0, size, size,
                                screen.height - size *2)
        self.right = pygame.Rect(screen.width - size, size,
                                 size, screen.height - size * 2)
        self.up = pygame.Rect(size, 0,
                              screen.width - size * 2, size)
        self.down = pygame.Rect(size, screen.height - size,
                                screen.width - size * 2, size)

        # color of controller.  It is hidden by default
        blue = (0, 0, 255)

        self.leftbutton = pygame.Surface(self.left.size)
        self.rightbutton = pygame.Surface(self.right.size)
        self.upbutton = pygame.Surface(self.up.size)
        self.downbutton = pygame.Surface(self.down.size)
        self.buttons = {self.leftbutton: self.left, self.rightbutton: self.right,
                   self.upbutton: self.up, self.downbutton: self.down}
        for button in self.buttons:
            button.fill(blue)
            button.set_alpha(40)
