__author__ = 'craig'


"""
Steps to build a 2D tile map game
---------------------------------
1. Mapfile
    Example: The function load_map(filename)
    1.1 read json map file from disk
    1.2 load into python dictionary


2. Tilesets
    Example: class Tileset()
    2.1 extract list of tilesets from map dictionary
    Example: Tileset.load() will open the tileset files and create a list
of surfaces that hold all the tilesets.

    2.2 for each tileset, slice a 32x32 pixel square
    Example: Tileset.slice_tiles2(tileset_images)

    2.3 load each tile into a dictionary of all tiles from all the tilesets
    Example: Also handled in Tileset.slice_tiles2(tileset_images)

3. Display Tiles
    Example: class Layer()

4.Display Player

5.Check for touchscreen input and set direction (or keyboard on desktop computer)
    Example: class EventHandler()
    5.1 Keyboard input using arrow keys
      Example: EventHandler.set_direction
    5.2 touchscreen input
        - create virtual game controller
        Example: class GameController()
        - check for touchscreen input with virtual game controller
        Example: EventHandler.mouse_direction()

6. Move Tiles
    Example: Layer.update_pos()

7. Check boundaries
    Example: Layer.calculate_map_boundary() and Layer.check_boundary()

8. Handle collision
    Example: Layer.check_collision()
"""

import json, pygame, sys
import pprint


try:
    import android
except ImportError:
    android = None
if android:
    android.init()
    android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)

# When the home screen is pressed, pause your Android game
# so it doesn't keep running in the background
# This didn't seem to be working in my last test.
# I'm leaving it in for now.

def check_for_pause():
    if android.check_pause():
        android.wait_for_resume()


class GameScreen:
    def __init__(self):
        self.width = 480
        self.height = 320

def load_map(filename):
    """
    This takes a file written with Tiled that contains maps in JSON format.
    Tiled is freely available here:
    http://www.mapeditor.org/

    returns a dictionary of the map data.

    """
    mapfile = open(filename)
    jsondata = mapfile.read()
    mapdict = json.loads(jsondata)
    return(mapdict)

class Tileset():
    """
    In the JSON map that is created with the tile map editor, Tiled, "tilesets" is one of the top-level
    keys.  This contains a list of dictionaries, one element for each tileset.
    Each tileset is an image, often in PNG format, that contains many pictures of objects such as
    trees, grass, rocks, fences, and water.  Each tile in the set is usually a square that is 32x32
    pixels.  The size of each tile could be bigger or smaller than 32.

    This class will slice up the tilesheet into individual tiles and then stare each tile into a
    list.
    """
    def __init__(self, mapdict):
        self.tilesets = mapdict["tilesets"]

    def load(self):
        """
        Using the key "image" get the name of the file for each tileset.
        Load the graphic file into the program as a surface.
        """
        tileset_images = []
        for tilesetdata in self.tilesets:

            tilesetfile = tilesetdata["image"]
            tileset = pygame.image.load(tilesetfile)
            tileset_images.append(tileset)
        return(tileset_images)


    def slice_tiles2(self, tileset_images):
        """
        Slices up the tileset and returns a dictionary of all tiles in all layers.
        Accepts: tileset_images (list of all tileset surfaces)
        Returns: tiles (dictionary containing the tile_id as the key and
        the surface of each individual tile.  All the tiles for all the tilesets
        are stored in a single dictionary.

        Use the dictionary when you read in the layers of the JSON mapfile
        produced by Tiled.  In each layer, there is a "data" key that lists
        all the tiles on the map.  With this key/value dictionary, you can
        match each tile with the number in the "data" list.
        """
        tile_id = 1
        tiles = {}
        for tileset_image in tileset_images:
            tileset_width = tileset_image.get_width()
            tileset_height = tileset_image.get_height()
            for y in range (0, tileset_height, 32):
                for x in range (0, tileset_width, 32):
                    rect = pygame.Rect(x, y, 32, 32)
                    tile = tileset_image.subsurface(rect)
                    tiles.update({tile_id: tile})
                    tile_id +=1
        return(tiles)


class Layer():
    def __init__(self, mapdict, tiles):
        self.layers = mapdict["layers"]
        self.tiles = tiles
        self.width = mapdict["width"]
        self.height = mapdict["height"]
        self.tilewidth = tiles[1].get_width()
        self.tileheight = tiles[1].get_height()
        self.speed = 1
        screen = GameScreen()
        self.screensize = (screen.width, screen.height)
        self.mapwidth = self.width * self.tilewidth
        self.mapheight = self.height * self.tileheight

    def load_collision(self):
        """
        Look for a user-defined property of the layer called, "collision".
        If this is found, then add the rectangle to a collision list.

        If the data for the layer contains a zero "0" element, then do not
        save the blank element to the list.

        Usage: Layer.load_collision()

        Returns: collision_list
        """
        collision_list = []
        for layer in self.layers:
            data = layer["data"]
            if layer.has_key("properties"):
                properties = layer["properties"]
                if properties.has_key("collision"):
                    collision_key = properties["collision"]
                    if collision_key == "1":
                        collision_index = 0
                        for y in range (0, self.mapheight, 32):
                            for x in range (0, self.mapwidth, 32):
                                if data[collision_index] != 0:
                                    collision_rect = pygame.Rect(x, y, 32, 32)
                                    collision_list.append(collision_rect)
                                collision_index +=1
        return(collision_list)

    def load2(self):
        """
        Creates a large surface that is the same size as the entire map.
        For each layer in the map, a new surface is created.  The
        surfaces are merged together with blit.

        The layers are built up by blitting 32x32 pixel tiles
        across each row of the map.

        The position of each tile is generated by a nested for loop
        for y and x coordinates.

        Each element of the list data contains a number that is the
        "key" or "id" of each tile.  For example, if the tilesheet
        has 120 tiles (12 tiles across and 10 deep), then there will be
        120 "keys" or "id" numbers.  If there is a second tileset that
        contains 200 additional tiles, then there will be 320 keys.

        Once the program knows the key from reading in the data for
        each layer, it uses the tileset_key to access the value in the
        tiles dictionary.   The value is an image, or surface, of
        the tile that is going to be blitted onto the map.
        """
        combined_layers = pygame.Surface((self.mapwidth, self.mapheight))
        layer_num = 1

        for layer in self.layers:
            # for each layer, read in the list of numbers for the map
            # and load into a list.  The key "data" is used to access
            # the information for each layer
            data = layer["data"]
            # create a blank layer that is the size of the entire
            # map.
            current_layer = pygame.Surface((self.mapwidth, self.mapheight))
            data_list_element = 0
            for y in range (0, self.mapheight, 32):
                for x in range (0, self.mapwidth, 32):
                    tileset_key = data[data_list_element]
                    if tileset_key != 0:
                        current_layer.blit(self.tiles[tileset_key], (x, y))
                    data_list_element += 1
            current_layer.set_colorkey((0,0,0))
            # the line below is for testing
            pygame.image.save(current_layer, "test_output/layer_{}.png".format(layer_num))
            combined_layers.blit(current_layer, (0, 0))
            layer_num += 1
        # line below is for testing.
        pygame.image.save(combined_layers, "test_output/map_output.png")
        return(combined_layers)

    def calculate_map_boundary(self):
        """
        Track the upper left hand corner of the entire map.

        Remember that the map is bigger than the phone screen.
        The upper left coordinate will always be in negative numbers
        since the upper left corner will be off the visible area
        of the phone screen.

        If the map starts off with the upper left corner in the upper
        left corner of the screen, then the position is [0,0]
        If the player starts off 320 (10 tiles) to the right,
        the position is [-320, 0].  If the player is traveling left,
        the x coordinate pos[0] should never be greater than 0.
        It always needs to be a negative value.

        Does not return any values.
        """
        self.buffer = self.speed + 1
        self.map_right_boundary = self.screensize[0] - self.mapwidth + self.buffer
        self.map_left_boundary = 0 - self.buffer
        self.map_up_boundary = 0 - self.buffer
        self.map_down_boundary = self.screensize[1] - self.mapheight + self.buffer

    def check_boundary(self, direction, pos):
        clear_to_move = True
        if direction == "left" and pos[0] > self.map_left_boundary:
            clear_to_move = False
        if direction == "right" and pos[0] < self.map_right_boundary:
            clear_to_move = False
        if direction == "up" and pos[1] > self.map_up_boundary:
            clear_to_move = False
        if direction == "down" and pos[1] < self.map_down_boundary:
            clear_to_move = False
        return(clear_to_move)

    def check_collision(self, direction, collision_list, clear_to_move):
        """
        Check if player is about to collide with a rectangle in the
        list rectangles that have collision enabled.  The list is called
        collision_list
        """
        player_rect = pygame.Rect(24, 24, 0, 0)
        player_rect.center = (self.screensize[0]/2, self.screensize[1]/2)
        for rect in collision_list:
            rect_tmp = rect.copy()
            if direction =="left":
                rect_tmp.centerx += (self.buffer * 2)
            elif direction == "right":
                rect_tmp.centerx -= (self.buffer *2)
            elif direction == "up":
                rect_tmp.centery += (self.buffer * 2)
            elif direction == "down":
                rect_tmp.centery -= (self.buffer * 2)
            if rect_tmp.colliderect(player_rect):
                clear_to_move = False
        return(clear_to_move)

    def update_pos(self, pos, direction, collision_list):
        clear_to_move = self.check_boundary(direction, pos)
        clear_to_move = self.check_collision(direction, collision_list, clear_to_move)

        if clear_to_move:
            if direction == "right":
                pos[0] -= self.speed
                for rect in collision_list:
                    rect.centerx -= self.speed
            elif direction == "left":
                pos[0] += self.speed
                for rect in collision_list:
                    rect.centerx += self.speed
            elif direction == "down":
                pos[1] -= self.speed
                for rect in collision_list:
                    rect.centery -= self.speed
            elif direction == "up":
                pos[1] += self.speed
                for rect in collision_list:
                    rect.centery += self.speed
        return(pos, collision_list)





class RunTest():
    def showdata(self, mapdict):
        """
        Don't use this.  It was created to run some tests.
        Takes a dictionary of map data, converted from Tiled data.
        returns a pygame.Surface that is the entire tileset.
        """
        mapkeys =mapdict.keys()
        pp = pprint.PrettyPrinter(indent=4)
        print ("\n\nThere are usually 9 primary keys in the json file produced by Tiled.\n")
        print("The keys in your map file are:")
        pp.pprint(mapkeys)
        tilesets = mapdict["tilesets"]
        print("\nYour map file uses {} tilesets\n".format(len(tilesets)))
        tilesetdata = tilesets[0]
        print("The keys in the tileset are:")
        pp.pprint(tilesetdata.keys())
        tilesetfile = tilesetdata["image"]
        tileset = pygame.image.load(tilesetfile)
        return(tileset)

    def showcollision(self, collision_list, screen):
        for rect in collision_list:
            tile = pygame.Surface((32, 32))
            tile.fill((255, 0, 0))
            tile.set_alpha(70)
            screen.blit(tile, rect)
        return(screen)

    def showcontroller(self, virtual_controller, screen):
        for button in virtual_controller.buttons:
            screen.blit(button, virtual_controller.buttons[button])


class EventHandler():
    def quit_game(self, event):
        if event.type == pygame.QUIT or \
                (event.type == pygame.KEYDOWN and
                         event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

    def set_direction(self, event, direction, virtual_game_controller):
        self.virtual_game_controller = virtual_game_controller
        direction = self.mouse_direction(direction)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction = "right"
            elif event.key == pygame.K_LEFT:
                direction = "left"
            elif event.key == pygame.K_UP:
                direction = "up"
            elif event.key == pygame.K_DOWN:
                direction = "down"
        return(direction)

    def mouse_direction(self, direction):
        """
        sets direction based on touchscreen input.
        accepts current direction.  Checks for mouse position (same as touchscreen)
        and then returns direction.
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.virtual_game_controller.left.collidepoint(mouse_pos):
            direction = "left"
        elif self.virtual_game_controller.right.collidepoint(mouse_pos):
            direction = "right"
        if self.virtual_game_controller.up.collidepoint(mouse_pos):
            direction = "up"
        elif self.virtual_game_controller.down.collidepoint(mouse_pos):
            direction = "down"
        return(direction)

class GameController():
    def __init__(self):
        screen = GameScreen()
        #adjust the size of the controller button.
        size = 100
        self.left = pygame.Rect(0, size, size,
                                screen.height - size *2)
        self.right = pygame.Rect(screen.width - size, size,
                                 size, screen.height - size * 2)
        self.up = pygame.Rect(size, 0,
                              screen.width - size * 2, size)
        self.down = pygame.Rect(size, screen.height - size,
                                screen.width - size * 2, size)

        # color of controller
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



