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
