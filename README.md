json_loader
===========
Example python json map loader for Tiled maps saved in json format.  The graphics mouse io are handled by Pygame.  the application is loaded onto Android phones with Pygame Subset for Android.

Click on the link below to see a video of the lesson's example code running on a Samsung Android phone.

http://youtu.be/tJ_O48oTpxk

The example was developed as part of the teaching curriculum for my 14 year old son.  

I originally created a video for him to learn how to use Tiled.  When I put it up on YouTube, several people commented on it and wanted the code for the example.  I decided to put the code up so that I could share it with people that watched the video.  This is the second version of the JSON loader code.  

In order to progress in our lesson and get some 2D game development experience, I have my son working on a JSON loader.  The lessons seem to be working so far.

http://pychildren.blogspot.com/2013/08/tiled-json-map-loader-example-code.html

To use this lesson, you will need:

 - Python
 - Pygame http://www.pygame.org/
 - Pygame Subset for Android http://pygame.renpy.org/
 - Tiled http://www.mapeditor.org/

If you're not putting the application on Android, you should check out Tiled TMX Loader.  Note that Pygame Subset for Android (pgs4a) doesn't work with the XML libraries and won't work with Tiled TMX Loader.  

Alternative TMX Loaders:
  - PyTMX https://github.com/bitcraft/PyTMX
  - pytmxloader https://code.google.com/p/pytmxloader/


<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html><head><title>Python: module main</title>
</head><body bgcolor="#f0f0f8">

<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="heading">
<tr bgcolor="#7799ee">
<td valign=bottom>&nbsp;<br>
<font color="#ffffff" face="helvetica, arial">&nbsp;<br><big><big><strong>main</strong></big></big></font></td
><td align=right valign=bottom
><font color="#ffffff" face="helvetica, arial"><a href=".">index</a><br><a href="file:/Users/coda/Documents/python/practice/2013_December/mapper/main.py">/Users/coda/Documents/python/practice/2013_December/mapper/main.py</a></font></td></tr></table>
    <p><tt>This&nbsp;is&nbsp;a&nbsp;test&nbsp;program&nbsp;to&nbsp;teach&nbsp;my&nbsp;teenage&nbsp;son&nbsp;to&nbsp;program&nbsp;Android<br>
games&nbsp;in&nbsp;Python&nbsp;for&nbsp;his&nbsp;mobile&nbsp;phone.<br>
&nbsp;<br>
Additional&nbsp;information&nbsp;is&nbsp;available&nbsp;at&nbsp;<a href="http://pychildren.blogspot.com">http://pychildren.blogspot.com</a><br>
&nbsp;<br>
Steps&nbsp;to&nbsp;build&nbsp;a&nbsp;2D&nbsp;tile&nbsp;map&nbsp;game<br>
&nbsp;&nbsp;&nbsp;1)&nbsp;Mapfile<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;a)&nbsp;read&nbsp;json&nbsp;map&nbsp;file&nbsp;from&nbsp;disk<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;b)&nbsp;load&nbsp;into&nbsp;python&nbsp;dictionary<br>
&nbsp;<br>
&nbsp;&nbsp;&nbsp;2)&nbsp;Tilesets<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;a)&nbsp;extract&nbsp;list&nbsp;of&nbsp;tilesets&nbsp;from&nbsp;map&nbsp;dictionary<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;b)&nbsp;for&nbsp;each&nbsp;tileset,&nbsp;slice&nbsp;a&nbsp;32x32&nbsp;pixel&nbsp;square<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;c)&nbsp;load&nbsp;each&nbsp;tile&nbsp;into&nbsp;a&nbsp;list&nbsp;of&nbsp;all&nbsp;tiles&nbsp;from&nbsp;all&nbsp;the&nbsp;tilesets<br>
&nbsp;<br>
&nbsp;&nbsp;&nbsp;3)&nbsp;Display&nbsp;Tiles<br>
&nbsp;&nbsp;&nbsp;4)&nbsp;Display&nbsp;Player<br>
&nbsp;&nbsp;&nbsp;5)&nbsp;Move&nbsp;Tiles<br>
&nbsp;&nbsp;&nbsp;5)&nbsp;Handle&nbsp;collision</tt></p>
<p>
<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="section">
<tr bgcolor="#aa55cc">
<td colspan=3 valign=bottom>&nbsp;<br>
<font color="#ffffff" face="helvetica, arial"><big><strong>Modules</strong></big></font></td></tr>
    
<tr><td bgcolor="#aa55cc"><tt>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</tt></td><td>&nbsp;</td>
<td width="100%"><table width="100%" summary="list"><tr><td width="25%" valign=top><a href="json.html">json</a><br>
</td><td width="25%" valign=top><a href="pprint.html">pprint</a><br>
</td><td width="25%" valign=top><a href="pygame.html">pygame</a><br>
</td><td width="25%" valign=top><a href="sys.html">sys</a><br>
</td></tr></table></td></tr></table><p>
<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="section">
<tr bgcolor="#ee77aa">
<td colspan=3 valign=bottom>&nbsp;<br>
<font color="#ffffff" face="helvetica, arial"><big><strong>Classes</strong></big></font></td></tr>
    
<tr><td bgcolor="#ee77aa"><tt>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</tt></td><td>&nbsp;</td>
<td width="100%"><dl>
<dt><font face="helvetica, arial"><a href="main.html#EventHandler">EventHandler</a>
</font></dt><dt><font face="helvetica, arial"><a href="main.html#Layer">Layer</a>
</font></dt><dt><font face="helvetica, arial"><a href="main.html#Tileset">Tileset</a>
</font></dt></dl>
 <p>
<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="section">
<tr bgcolor="#ffc8d8">
<td colspan=3 valign=bottom>&nbsp;<br>
<font color="#000000" face="helvetica, arial"><a name="EventHandler">class <strong>EventHandler</strong></a></font></td></tr>
    
<tr><td bgcolor="#ffc8d8"><tt>&nbsp;&nbsp;&nbsp;</tt></td><td>&nbsp;</td>
<td width="100%">Methods defined here:<br>
<dl><dt><a name="EventHandler-quit_game"><strong>quit_game</strong></a>(self, event)</dt></dl>

<dl><dt><a name="EventHandler-set_direction"><strong>set_direction</strong></a>(self, event, direction)</dt></dl>

</td></tr></table> <p>
<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="section">
<tr bgcolor="#ffc8d8">
<td colspan=3 valign=bottom>&nbsp;<br>
<font color="#000000" face="helvetica, arial"><a name="Layer">class <strong>Layer</strong></a></font></td></tr>
    
<tr><td bgcolor="#ffc8d8"><tt>&nbsp;&nbsp;&nbsp;</tt></td><td>&nbsp;</td>
<td width="100%">Methods defined here:<br>
<dl><dt><a name="Layer-__init__"><strong>__init__</strong></a>(self, mapdict, tiles)</dt></dl>

<dl><dt><a name="Layer-calculate_map_boundary"><strong>calculate_map_boundary</strong></a>(self)</dt><dd><tt>Track&nbsp;the&nbsp;upper&nbsp;left&nbsp;hand&nbsp;corner&nbsp;of&nbsp;the&nbsp;entire&nbsp;map.<br>
&nbsp;<br>
Remember&nbsp;that&nbsp;the&nbsp;map&nbsp;is&nbsp;bigger&nbsp;than&nbsp;the&nbsp;phone&nbsp;screen.&nbsp;&nbsp;The&nbsp;upper&nbsp;left&nbsp;coordinate&nbsp;will<br>
always&nbsp;be&nbsp;in&nbsp;negative&nbsp;numbers&nbsp;since&nbsp;the&nbsp;upper&nbsp;left&nbsp;corner&nbsp;will&nbsp;be&nbsp;off&nbsp;the&nbsp;visible&nbsp;area<br>
of&nbsp;the&nbsp;phone&nbsp;screen.<br>
&nbsp;<br>
If&nbsp;the&nbsp;map&nbsp;starts&nbsp;off&nbsp;with&nbsp;the<br>
upper&nbsp;left&nbsp;corner&nbsp;in&nbsp;the&nbsp;upper&nbsp;left&nbsp;corner&nbsp;of&nbsp;the&nbsp;screen,&nbsp;then&nbsp;the&nbsp;position&nbsp;is&nbsp;[0,0]<br>
If&nbsp;the&nbsp;player&nbsp;starts&nbsp;off&nbsp;320&nbsp;(10&nbsp;tiles)&nbsp;to&nbsp;the&nbsp;right,&nbsp;the&nbsp;position&nbsp;is&nbsp;[-320,&nbsp;0].<br>
If&nbsp;the&nbsp;player&nbsp;is&nbsp;traveling&nbsp;left,&nbsp;the&nbsp;x&nbsp;coordinate&nbsp;pos[0]&nbsp;should&nbsp;never&nbsp;be&nbsp;greater&nbsp;than&nbsp;0.<br>
It&nbsp;always&nbsp;needs&nbsp;to&nbsp;be&nbsp;a&nbsp;negative&nbsp;value.</tt></dd></dl>

<dl><dt><a name="Layer-check_boundary"><strong>check_boundary</strong></a>(self, direction, pos)</dt></dl>

<dl><dt><a name="Layer-check_collision"><strong>check_collision</strong></a>(self, direction, collision_list, clear_to_move)</dt><dd><tt>Check&nbsp;if&nbsp;player&nbsp;is&nbsp;about&nbsp;to&nbsp;collide&nbsp;with&nbsp;a&nbsp;rectangle&nbsp;in&nbsp;the<br>
list&nbsp;rectangles&nbsp;that&nbsp;have&nbsp;collision&nbsp;enabled.&nbsp;&nbsp;The&nbsp;list&nbsp;is&nbsp;called<br>
collision_list</tt></dd></dl>

<dl><dt><a name="Layer-load"><strong>load</strong></a>(self)</dt></dl>

<dl><dt><a name="Layer-update_pos"><strong>update_pos</strong></a>(self, pos, direction, collision_list)</dt></dl>

</td></tr></table> <p>
<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="section">
<tr bgcolor="#ffc8d8">
<td colspan=3 valign=bottom>&nbsp;<br>
<font color="#000000" face="helvetica, arial"><a name="Tileset">class <strong>Tileset</strong></a></font></td></tr>
    
<tr bgcolor="#ffc8d8"><td rowspan=2><tt>&nbsp;&nbsp;&nbsp;</tt></td>
<td colspan=2><tt>In&nbsp;the&nbsp;JSON&nbsp;map&nbsp;that&nbsp;is&nbsp;created&nbsp;with&nbsp;the&nbsp;tile&nbsp;map&nbsp;editor,&nbsp;Tiled,&nbsp;"tilesets"&nbsp;is&nbsp;one&nbsp;of&nbsp;the&nbsp;top-level<br>
keys.&nbsp;&nbsp;This&nbsp;contains&nbsp;a&nbsp;list&nbsp;of&nbsp;dictionaries,&nbsp;one&nbsp;element&nbsp;for&nbsp;each&nbsp;tileset.<br>
Each&nbsp;tileset&nbsp;is&nbsp;an&nbsp;image,&nbsp;often&nbsp;in&nbsp;PNG&nbsp;format,&nbsp;that&nbsp;contains&nbsp;many&nbsp;pictures&nbsp;of&nbsp;objects&nbsp;such&nbsp;as<br>
trees,&nbsp;grass,&nbsp;rocks,&nbsp;fences,&nbsp;and&nbsp;water.&nbsp;&nbsp;Each&nbsp;tile&nbsp;in&nbsp;the&nbsp;set&nbsp;is&nbsp;usually&nbsp;a&nbsp;square&nbsp;that&nbsp;is&nbsp;32x32<br>
pixels.&nbsp;&nbsp;The&nbsp;size&nbsp;of&nbsp;each&nbsp;tile&nbsp;could&nbsp;be&nbsp;bigger&nbsp;or&nbsp;larger&nbsp;than&nbsp;32.<br>
&nbsp;<br>
This&nbsp;class&nbsp;will&nbsp;slice&nbsp;up&nbsp;the&nbsp;tilesheet&nbsp;into&nbsp;individual&nbsp;tiles&nbsp;and&nbsp;then&nbsp;stare&nbsp;each&nbsp;tile&nbsp;into&nbsp;a<br>
list.<br>&nbsp;</tt></td></tr>
<tr><td>&nbsp;</td>
<td width="100%">Methods defined here:<br>
<dl><dt><a name="Tileset-__init__"><strong>__init__</strong></a>(self, mapdict)</dt></dl>

<dl><dt><a name="Tileset-load"><strong>load</strong></a>(self)</dt><dd><tt>Using&nbsp;the&nbsp;key&nbsp;"image"&nbsp;get&nbsp;the&nbsp;name&nbsp;of&nbsp;the&nbsp;file&nbsp;for&nbsp;each&nbsp;tileset.<br>
Load&nbsp;the&nbsp;graphic&nbsp;file&nbsp;into&nbsp;the&nbsp;program&nbsp;as&nbsp;a&nbsp;surface.</tt></dd></dl>

<dl><dt><a name="Tileset-slice_tiles"><strong>slice_tiles</strong></a>(self, tileset_images)</dt><dd><tt>Slices&nbsp;up&nbsp;the&nbsp;tileset&nbsp;and&nbsp;returns&nbsp;a&nbsp;list&nbsp;of&nbsp;all&nbsp;tiles&nbsp;in&nbsp;all&nbsp;layers.</tt></dd></dl>

</td></tr></table></td></tr></table><p>
<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="section">
<tr bgcolor="#eeaa77">
<td colspan=3 valign=bottom>&nbsp;<br>
<font color="#ffffff" face="helvetica, arial"><big><strong>Functions</strong></big></font></td></tr>
    
<tr><td bgcolor="#eeaa77"><tt>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</tt></td><td>&nbsp;</td>
<td width="100%"><dl><dt><a name="-load_map"><strong>load_map</strong></a>(filename)</dt><dd><tt>This&nbsp;takes&nbsp;a&nbsp;file&nbsp;written&nbsp;with&nbsp;Tiled&nbsp;that&nbsp;contains&nbsp;maps&nbsp;in&nbsp;JSON&nbsp;format.<br>
Tiled&nbsp;is&nbsp;freely&nbsp;available&nbsp;here:<br>
<a href="http://www.mapeditor.org/">http://www.mapeditor.org/</a><br>
&nbsp;<br>
returns&nbsp;a&nbsp;dictionary&nbsp;of&nbsp;the&nbsp;map&nbsp;data.</tt></dd></dl>
 <dl><dt><a name="-main"><strong>main</strong></a>()</dt></dl>
 <dl><dt><a name="-run_test"><strong>run_test</strong></a>(mapdict)</dt><dd><tt>Don't&nbsp;use&nbsp;this.&nbsp;&nbsp;It&nbsp;was&nbsp;created&nbsp;to&nbsp;run&nbsp;some&nbsp;tests.<br>
Takes&nbsp;a&nbsp;dictionary&nbsp;of&nbsp;map&nbsp;data,&nbsp;converted&nbsp;from&nbsp;Tiled&nbsp;data.<br>
returns&nbsp;a&nbsp;pygame.Surface&nbsp;that&nbsp;is&nbsp;the&nbsp;entire&nbsp;tileset.</tt></dd></dl>
</td></tr></table><p>
<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="section">
<tr bgcolor="#55aa55">
<td colspan=3 valign=bottom>&nbsp;<br>
<font color="#ffffff" face="helvetica, arial"><big><strong>Data</strong></big></font></td></tr>
    
<tr><td bgcolor="#55aa55"><tt>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</tt></td><td>&nbsp;</td>
<td width="100%"><strong>RUNTEST</strong> = True</td></tr></table>
</body></html>