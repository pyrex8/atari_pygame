# atari.py
The module atari.py was created as an aid for the creation of atari 2600 VCS like games with graphics and sound routines using python and pygame.

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
```
from atari import *
initialization
pygame loop
```

command list
------------

Note: There are 160 X pixels and 104 Y pixels. There are suppose to be approximaetly 192 lines on an NTSC screen. To simplify the functions and make the pixels symetrical two lines are used. This should equate to 192/2 or 96 Y pixels, but replicating combat required 104 pixels to fit the complete playfield. The actual visable area on a US varied so some games may have ran over the 192 line rule of thumb. Some atari games use non symetical "pixels" and example is Space Invaders. The added complexity is that scan lines are interlaced so in reality the programmer had to get the next line on an alternate screen refresh. For now single line Y pixels are not supported.


*sound(audv, audf, audc, length)*

The atari had two channels of audio. This function just has one channel for now. I just barely have the audio working so I'm not sure if audv, audf, and audc map 1:1. Length is the number of samples. The sample rate is 31400Hz, so 1000 samples is 31.8 msec.

```
tank engine sound moving     
sound(8, 5, 2, 10000)
```


*init_switches()*

Sets up the repeat key function. ??? Questioning the logic of this even having a function or being placed here.

*update_switches()*

This only returns one key. This should return multiple key presses espcially for two player games. This is the standard Stella keymap for two players, minus the right shift for player 0 fire. Player 0 is the arrow keys and space bar. Player 1 is y,g,jh and f for fire. 

*reset_collision()*

Use this at the top of the main loop to reset collision detection, otherwise collisions are sticky.

*update_collision(new_object, x, y)*

Used by drawing routines to as pixels are drawn. Doesn't need to be called externally by user.

*test_for_object(test_object, x, y)*

This is an extra hook so that a program can test for a wall. This wasn't available on an atari. It is in the module just in case it is useful.

*get_collision(first_object, second_object)*

This is equivalent to the atari collision registers. Allows collision test between two objects (P0, M0, P1, M0, ,PF, BL) 0 = no collision, 1 = collision.

*game_title(name)*

Non Atari function, just for naming the pygame window.

*background(screen, y, height, color)*

This is equivalent to setting the background color register at scan line "y" and for the next "height" scan lines (remember they are interlaced).

*playfield_collision(x, y)*

This is a repetative process used in the code so it was turned into a function. Really just for internal code use.

*place_digit(screen, x, y, digit, color)*

A built in function to print digits using playfield graphics. This was one of the earliest and crudest scoring methods. On an atari this requied ROM and quite a bit of coding work. This function is to take the tedium out of doing this manually. Since this is drawn as a playfield object, collision with other objects is possible.

*number(screen, x, y, value, color)*

Takes the place_digit() function one step further by printing a complete integer.

*playfield(screen, y, height, data, color, left, right)*

This is the playfield drawing function. To make life easier on the programmer the 20 bit data of a half playfield is not flipped like the atari 2600. The bits are WYSWYG. The playfield function can be used to draw a half playfield on either side, a mirrored or repeated graphic using the left and right values: 0 = off, 1 = on, non inverted, and 2 = inverted.
Player data is expected to be 20 bits wide as a string of characters. 1 bits are are represented as upper case X. any other character can be a zero, a space or a "." are the most commonly used characters in disassembled ROMS. 

```
 pfield =    ['XXXXXXXXXXXXXXXXXXXX' 
             ,'X..................X' 
             ,'X..................X' 
             ,'X...................' 
             ,'X.....XXX...........' 
             ,'X...................' 
             ,'X.............XXX...' 
             ,'X.............X.....' 
             ,'X....XX.............' 
             ,'X.....X.............' 
             ,'X.....X.............' 
             ,'X.....X...XX........']
```

*ball(screen, x, y, width, height, color)*

Ball is simplified by having an x, y, width, and height. The only "valid" widths are 1, 2, and 4 but the function is not limited to this so it is up to the programming to decide whether to enforce restrictions that emulate an atari 2600.

*missile0(screen, x, y, width, height, color)*

Identical to ball function.

*missile1(screen, x, y, width, height, color)*

Identical to ball function.

*player0(screen, x, y, data, color)*

Player data is expected to be 8 bits wide as a string of characters. 1 bits are are represented as upper case X. any other character can be a zero, a space or a "." are the most commonly used characters in disassembled ROMS.   

```
tank =       ['        '
             ,'XXXXXX  ' 
             ,'XXXXXX  ' 
             ,'  XXX   ' 
             ,'  XXXXXX' 
             ,'  XXX   ' 
             ,'XXXXXX  ' 
             ,'XXXXXX  ']
```


screenshot from combat.py 
------------

![alt text](https://github.com/pyrex8/atari/blob/master/combat_screen_shot.png "combat.py screen shot")






example code drawing pacman 
------------

```
from atari import *
import math 

pacman =    ['  XXX   '
            ,' XX XX  '
            ,'XXXXXXX '
            ,'    XXX '
            ,'XXXXXXX '
            ,' XXXXX  '
            ,'  XXX   ']

# end data
game_title('pacman')
move = ''

while move != 'quit':
    reset_collision()
    background(screen, 0, WINDOWHEIGHT, black)

    # Game code starts here
    move = update_switches()

    player0(screen, SCREEN_X/2 - 4 , SCREEN_Y/2 - 4, pacman, yellow)

    # Game code ends here
    pygame.display.flip()
    clock.tick(FRAME_RATE)

stream.close()
p.terminate()    
pygame.quit()
```


![alt text](https://github.com/pyrex8/atari/blob/master/pacman_screen_shot.png "combat.py screen shot")

