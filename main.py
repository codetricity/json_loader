"""
This is a test program to teach my teenage son to program Android
games in Python for his mobile phone.

Additional information is available at:
  http://github.com/codetricity/json_loader

The goal of the lesson is to build a JSON map loader that is
produced from Tiled.  Once the JSON loader is built, it can be
used to create a variety of games.

In addition to json_loader, you will need to have Python 2.7 and
Pygame 1.9.1 installed.  Pygame does not work with Python 3.

Follow my son's progress:
http://pychildren.blogspot.com

"""

__author__ = 'craig'
import pygame
import json_loader



def main():

    # initialize pygame
    pygame.init()
    # set screen size of phone or desktop window.  Adjust to your phone
    screen = pygame.display.set_mode((480, 320))
    pygame.display.set_caption("Use keyboard arrow keys or mouse.  Press TEST to toggle overlay")
    

    # game framerate.  Higher number is faster
    FPS = 40

    # change the file names to your player graphic and map file
    player_image_file = "img/girl.png"
    map_file = "maps/larger_map.json"

    # change to False (with capital F) to turn off red squares over
    # collision rectangles
    TESTING = True

    #initialize json loader, build tileset list, load player graphic
    initial = json_loader.Initialize(screen, TESTING, map_file, player_image_file)

    # initialize position of player when game first starts
    map = json_loader.Map(initial)
    map.move(-200, 0)

    # handle events such as keyboard / touchscreen presses
    event = json_loader.Event(initial)
    clock = pygame.time.Clock()


    while True:
        event.update()
        map.update(event.direction)
        map.display(screen)
        clock.tick(FPS)
        pygame.display.update()

if __name__ == "__main__":
    main()
