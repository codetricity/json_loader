"""
This is a test program to teach my teenage son to program Android
games in Python for his mobile phone.

Additional information is available at http://pychildren.blogspot.com

Steps to build a 2D tile map game
   1) Mapfile
      a) read json map file from disk
      b) load into python dictionary

   2) Tilesets
      a) extract list of tilesets from map dictionary
      b) for each tileset, slice a 32x32 pixel square
      c) load each tile into a list of all tiles from all the tilesets

   3) Display Tiles
   4) Display Player
   5) Move Tiles
   5) Handle collision
"""

import json, pygame, sys
import pprint

RUNTEST = True

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
    pixels.  The size of each tile could be bigger or larger than 32.

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

    def slice_tiles(self, tileset_images):
        """
        Slices up the tileset and returns a list of all tiles in all layers.
        """
        tiles = []
        for tileset_image in tileset_images:
            for y in range (0, 1024, 32):
                for x in range (0, 1024, 32):
                    rect = pygame.Rect(x, y, 32, 32)
                    tile = tileset_image.subsurface(rect)
                    tiles.append(tile)
        return(tiles)

class Layer():
    def __init__(self, mapdict, tiles):
        self.layers = mapdict["layers"]
        self.tiles = tiles
        self.width = mapdict["width"]
        self.height = mapdict["height"]
        self.tilewidth = tiles[0].get_width()
        self.tileheight = tiles[0].get_height()
        self.speed = 1
        self.screensize = (480, 320)


    def load(self):
        self.mapwidth = self.width * self.tilewidth
        self.mapheight = self.height * self.tileheight
        combined_layers = pygame.Surface((self.mapwidth, self.mapheight))
        collision_list = []
        layer_num = 1
        for layer in self.layers:
            full_map_surface = pygame.Surface((self.width * self.tilewidth, self.height * self.tileheight))
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
#                                    print('found collision rectangle')
                                    collision_rect = pygame.Rect(x, y, 32, 32)
                                    collision_list.append(collision_rect)
                                collision_index +=1
            x = 0
            y = 0
            for id in data:
                if id != 0:
                    gid = id -1
                    full_map_surface.blit(self.tiles[gid], (x, y))
                if x < self.width * (self.tilewidth -1):
                    x += self.tilewidth
                else:
                    x = 0
                    y += self.tileheight
            #pygame.image.save(full_map_surface, "layer_{}.png".format(layer_num))
            full_map_surface.set_colorkey((0,0,0))
            combined_layers.blit(full_map_surface, (0,0))
            #pygame.image.save(combined_layers, "map_output.png")

            layer_num += 1
        return(combined_layers, collision_list)

    def calculate_map_boundary(self):
        """
        Track the upper left hand corner of the entire map.

        Remember that the map is bigger than the phone screen.  The upper left coordinate will
        always be in negative numbers since the upper left corner will be off the visible area
        of the phone screen.

        If the map starts off with the
        upper left corner in the upper left corner of the screen, then the position is [0,0]
        If the player starts off 320 (10 tiles) to the right, the position is [-320, 0].
        If the player is traveling left, the x coordinate pos[0] should never be greater than 0.
        It always needs to be a negative value.
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





def run_test(mapdict):
    """
    Don't use this.  It was created to run some tests.
    Takes a dictionary of map data, converted from Tiled data.
    returns a pygame.Surface that is the entire tileset.
    """
    mapkeys =mapdict.keys()
    tilesets = mapdict["tilesets"]
    tilesetdata = tilesets[0]
    tilesetfile = tilesetdata["image"]
    tileset = pygame.image.load(tilesetfile)
    return(tileset)

class EventHandler():
    def quit_game(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def set_direction(self, event, direction):
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

def main():
    pygame.init()

    SCREENSIZE = (480, 320)
    SCREEN = pygame.display.set_mode(SCREENSIZE)
    starting_position = [-220,-200]

    pos = starting_position
    direction = "stop"


    mapdict = load_map("larger_map.json")
    tilesets = Tileset(mapdict)

    tileset_images = tilesets.load()
    tiles = tilesets.slice_tiles(tileset_images)

    layers = Layer(mapdict, tiles)

    # this controls the speed of the player moving around the screen
    layers.speed = 3

    # the default screensize is 480, 320
    layers.screensize = SCREENSIZE
    combined_layers, collision_list = layers.load()
    for rect in collision_list:
        rect.centerx += starting_position[0]
        rect.centery += starting_position[1]
    layers.calculate_map_boundary()

    event_handler = EventHandler()


    player = pygame.image.load("img/girl.png").convert_alpha()
    player_rect = player.get_rect(center = SCREEN.get_rect().center)



    while True:
        for event in pygame.event.get():
            event_handler.quit_game(event)
            direction = event_handler.set_direction(event, direction)

        pos, collision_list = layers.update_pos(pos, direction, collision_list)

        SCREEN.blit(combined_layers, pos)

        for rect in collision_list:
            tile = pygame.Surface((32, 32))
            tile.fill((255, 0, 0))
            tile.set_alpha(70)
            SCREEN.blit(tile, rect)

        SCREEN.blit(player, player_rect)

        pygame.display.update()




if __name__ == "__main__":
    main()
