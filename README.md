# atari
python pygame module for aiding the creation of atari 2600 VCS like games with graphics and sound routines.

This is not an emulator. atari.py is the module. The example program is combat.py.

This has been tested on windows and ubuntu using python 2.7

atari.py is used in the example combat.py

dependencies
------------
- python 2.7
- pygame
- pyaudio

installation
------------
 - Download atari.py and combat.py into the same folder.
 - Run combat.py.

basic structure in combat.py
----------------------------
    from atari import *
    initialization
    pygame loop

command list
------------

*sound(audv, audf, audc, length)*

The atari had two channels of audio. This function just has one channel for now. I just barely have the audio working so I'm not sure if audv, audf, and audc map 1:1. Length is the number of samples. The sample rate is 31400Hz, so 1000 samples is 31.8 msec.

``# tank engine sound moving``      
``sound(8, 5, 2, 10000)``


*init_switches()*

Sets up the repeat key function. ??? Questioning the logic of this even having a function or being placed here.

*update_switches()*

This only returns one key. This should return multiple key presses espcially for two player games.

*reset_collision()*

Use this at the top of the main loop to reset collision detection, otherwise collisions are sticky.

*update_collision(new_object, x, y)*

Used by drawing routines to as pixels are drawn. Doesn't need to be called externally by user.

*test_for_object(test_object, x, y)*

This is an extra hook so that a program can test for a wall. This wasn't available on an atari. It is in the module just in case it is useful.

*get_collision(first_object, second_object)*

This is equivalent to the atari collision registers. Allows collision test between two objects (P0, M0, P1, M0, ,PF, BL) 0 = no collision, 1 = collision.

=================





=================


