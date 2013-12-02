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
<ul>
 <li> Python
 <li> Pygame http://www.pygame.org/
 <li> Pygame Subset for Android http://pygame.renpy.org/
 <li> Tiled http://www.mapeditor.org/
</ul>


execute the sample program with:

 $ python main.py

The ./doc directory contains documentation that is automatically generated with pydoc

The ./img directory contains graphics for two characters, a boy and and girl.  The girl is default.  To use the boy,

change the line below 
  player_filename = "img/girl.png"

to
 player_filename = "img/boy.png"

Set RUNTEST to False to turn off red colored squares over collision
objects.



Alternatives to JSON
--------------------
If you're not putting the application on Android, you should check out Tiled TMX Loader.  Note that Pygame Subset for Android (pgs4a) doesn't work with the XML libraries and won't work with Tiled TMX Loader.  

Alternative TMX Loaders:
  - PyTMX https://github.com/bitcraft/PyTMX
  - pytmxloader https://code.google.com/p/pytmxloader/


Steps to Build a 2D Tile Map Game
---------------------------------

1. Mapfile
   ..1. read json map file from disk
   ..2. load into python dictionary 

2. Tilesets 
   ..1. extract list of tilesets from map dictionary
   ..2. for each tileset, slice a 32x32 pixel square
   ..3. load each tile into a list of all tiles from all the tilesets

3. Display Tiles 

4. Display Player

5. Move Tiles

6. Handle collision
