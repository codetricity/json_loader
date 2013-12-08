json_loader
===========

Overview
--------
Example python json map loader for Tiled maps saved in json format.  The graphics mouse io are handled by Pygame.  the application is loaded onto Android phones with Pygame Subset for Android.

Click on the link below to see a video of the lesson's example code running on a Samsung Android phone.

http://youtu.be/tJ_O48oTpxk

The example was developed as part of the teaching curriculum for my 14 year old son.  

I originally created a video for him to learn how to use Tiled.  When I put it up on YouTube, several people commented on it and wanted the code for the example.  I decided to put the code up so that I could share it with people that watched the video.  This is the second version of the JSON loader code.  

In order to progress in our lesson and get some 2D game development experience, I have my son working on a JSON loader.  The lessons seem to be working so far.


Usage
-----

To use this lesson, you will need:

* Python
* Pygame http://www.pygame.org/
* Pygame Subset for Android http://pygame.renpy.org/
* Tiled http://www.mapeditor.org/



execute the sample program on your desktop with:

 $ python main.py

The ./doc directory contains documentation that is automatically generated with pydoc

To edit the sample program:

The ./img directory contains graphics for two characters, a boy and and girl.  The girl is default.  To use the boy,

change the line below 
  player_filename = "img/girl.png"

to
 player_filename = "img/boy.png"

Set runtest to False to turn off red colored squares over collision
objects.  If you set runtest to True, it will also display the
virtual onscreen controller icons.

In main.py change the map file:
  json_filename ="maps/NAME_OF_YOUR_MAP_FILE.json"

Your map file must be in JSON format.  You must set the properties
of the collision layer in your map file to "1".   All your tilesets must
be in maps/tilesets.

The PLAYER_START_POS constant is the initial position of the player
when the game starts.  If you set this to [0, 0], the player will be
in the upper left-hand quadrant of your map.  Use negative values to
start the player to the right on the map or down on the map.





Alternatives to JSON
--------------------
If you're not putting the application on Android, you should check out Tiled TMX Loader.  Note that Pygame Subset for Android (pgs4a) doesn't work with the XML libraries and won't work with Tiled TMX Loader.  

Alternative TMX Loaders:
  - PyTMX https://github.com/bitcraft/PyTMX
  - pytmxloader https://code.google.com/p/pytmxloader/


Steps to Build a 2D Tile Map Game
---------------------------------
Steps to build a 2D tile map game
   1) Mapfile
   Example: The function load_map(filename)
      a) read json map file from disk
      b) load into python dictionary


   2) Tilesets
   Example: class Tileset()
      a) extract list of tilesets from map dictionary
      Example:
      Tileset.load() will open the tileset files and create a list
      of surfaces that hold all the tilesets.

      b) for each tileset, slice a 32x32 pixel square
      Example:
      Tileset.slice_tiles2(tileset_images)

      c) load each tile into a dictionary of all tiles from all the tilesets
      Example:
      Also handled in Tileset.slice_tiles2(tileset_images)


   3) Display Tiles
   Example: class Layer()

   4) Display Player

   5) Check for touchscreen input and set direction (or keyboard on desktop computer)
   Example: class EventHandler()

   a) Keyboard input using arrow keys
      Example: EventHandler.set_direction
   b) touchscreen input
      - create virtual game controller
        Example: class GameController()
      - check for touchscreen input with virtual game controller
        Example: EventHandler.mouse_direction()

   6) Move Tiles
   Example: Layer.update_pos()

   7) Check boundaries
   Example: Layer.calculate_map_boundary() and Layer.check_boundary()

   8) Handle collision
   Example: Layer.check_collision()