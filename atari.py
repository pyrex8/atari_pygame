#!/usr/bin/env python
''' atari is a very simple module for replicating the atari VCS/2600 graphics 
and sound in pygame. It does not strickly enforce all the hardware limitations 
of the 2600. This is an attempt to make it easy to make 2600ish games in 
python.'''

__author__ = "Rex Allison"
__copyright__ = "Copyright 2016, Rex Allison"
__license__ = "MIT"


import pygame
import pyaudio
import array
import math
import time
import random

from pygame.locals import *

ZOOM = 2
SCALING = 2
SCREEN_X = 160
SCREEN_Y = 104

WINDOWWIDTH = SCREEN_X * SCALING * ZOOM
WINDOWHEIGHT = SCREEN_Y * SCALING * ZOOM
WINDOW_SIZE = (WINDOWWIDTH,WINDOWHEIGHT)

PIXEL = SCALING * ZOOM 
PF_PIXEL = 4* SCALING * ZOOM

FRAME_RATE = 30

NUMBER_OF_OBJECTS = 6
# bit xs for collison detection
# bl, pf, m1, p1, m0, p0
BL = 0
P0 = 1
M0 = 2
P1 = 3
M1 = 4
PF = 5

# Data from http://www.biglist.com/lists/stella/archives/200109/msg00285.html

colors_hex = [
    0x000000,0x404040,0x6C6C6C,0x909090,0xB0B0B0,0xC8C8C8,0xDCDCDC,0xECECEC,
    0x444400,0x646410,0x848424,0xA0A034,0xB8B840,0xD0D050,0xE8E85C,0xFCFC68,
    0x702800,0x844414,0x985C28,0xAC783C,0xBC8C4C,0xCCA05C,0xDCB468,0xECC878,
    0x841800,0x983418,0xAC5030,0xC06848,0xD0805C,0xE09470,0xECA880,0xFCBC94,
    0x880000,0x9C2020,0xB03C3C,0xC05858,0xD07070,0xE08888,0xECA0A0,0xFCB4B4,
    0x78005C,0x8C2074,0xA03C88,0xB0589C,0xC070B0,0xD084C0,0xDC9CD0,0xECB0E0,
    0x480078,0x602090,0x783CA4,0x8C58B8,0xA070CC,0xB484DC,0xC49CEC,0xD4B0FC,
    0x140084,0x302098,0x4C3CAC,0x6858C0,0x7C70D0,0x9488E0,0xA8A0EC,0xBCB4FC,
    0x000088,0x1C209C,0x3840B0,0x505CC0,0x6874D0,0x7C8CE0,0x90A4EC,0xA4B8FC,
    0x00187C,0x1C3890,0x3854A8,0x5070BC,0x6888CC,0x7C9CDC,0x90B4EC,0xA4C8FC,
    0x002C5C,0x1C4C78,0x386890,0x5084AC,0x689CC0,0x7CB4D4,0x90CCE8,0xA4E0FC,
    0x003C2C,0x1C5C48,0x387C64,0x509C80,0x68B494,0x7CD0AC,0x90E4C0,0xA4FCD4,
    0x003C00,0x205C20,0x407C40,0x5C9C5C,0x74B474,0x8CD08C,0xA4E4A4,0xB8FCB8,
    0x143800,0x345C1C,0x507C38,0x6C9850,0x84B468,0x9CCC7C,0xB4E490,0xC8FCA4,
    0x2C3000,0x4C501C,0x687034,0x848C4C,0x9CA864,0xB4C078,0xCCD488,0xE0EC9C,
    0x442800,0x644818,0x846830,0xA08444,0xB89C58,0xD0B46C,0xE8CC7C,0xFCE08C]

black = colors_hex[0]
white = colors_hex[7]
green = colors_hex[90]
red = colors_hex[33]
blue = colors_hex[65]
yellow = colors_hex[15]
cyan = colors_hex[60]
magenta = colors_hex[46]
grey = colors_hex[1]

digits = []

digits =    ['XXX'
            ,'X X'
            ,'X X'
            ,'X X'
            ,'XXX'

            ,'  X'
            ,'  X'
            ,'  X'
            ,'  X'
            ,'  X'

            ,'XXX'
            ,'  X'
            ,'XXX'
            ,'X  '
            ,'XXX'

            ,'XXX'
            ,'  X'
            ,'XXX'
            ,'  X'
            ,'XXX'

            ,'X X'
            ,'X X'
            ,'XXX'
            ,'  X'
            ,'  X'

            ,'XXX'
            ,'X  '
            ,'XXX'
            ,'  X'
            ,'XXX'

            ,'XXX'
            ,'X  '
            ,'XXX'
            ,'X X'
            ,'XXX'

            ,'XXX'
            ,'  X'
            ,'  X'
            ,'  X'
            ,'  X'

            ,'XXX'
            ,'X X'
            ,'XXX'
            ,'X X'
            ,'XXX'

            ,'XXX'
            ,'X X'
            ,'XXX'
            ,'  X'
            ,'XXX']




# 3.58MHz clock divided by 114
pixelclock = 3580000
# CPUclock = pixelclock/3
f1 = pixelclock/114
duration_ms = 300
samples = (f1/1000 *duration_ms)


# TIASOUND emulation package by Ron Fry
# from ATARI 2600 VCS SOUND FREQUENCY AND WAVEFORM GUIDE by Eckhard Stolberg
# Atari 2600 Music And Sound Programming Guide by Paul Slocum 
# The Atari 2600 Music and Sound Page, Random Terrain 

# Distortion Table AUDC0 and AUDC1 control register
# All scalled for pixelclock/114

# 0 = 1 (always high)
# 11 = 1

# 1 = 001010000111011 (Saw     sounds similar to a saw waveform)
# 2 = 001010000111011->0100000000000000000100000000000 (465 bits long) 
#(Engine  many 2600 games use this for an engine sound)
# 3 = 001010000111011->0010110011111000110111010100001 (465 bits long)

# 4 = 01 (Square  a high pitched square waveform)
# 5 = 01

# 6 = 1111111111111000000000000000000 (Bass    fat bass sound)
# 10 = 1111111111111000000000000000000

# 7 = 0010110011111000110111010100001 (Pitfall log sound in pitfall
#, low and buzzy)
# 9 = 0010110011111000110111010100001

# 8 = 511 bits long (white noise) (Noise   white noise)

# 12 through 15 use CPUclock/114 so stretch each bit by 3 to make 
# pixelclock/114 compatable
# 12 = 10 (Lead    lower pitch square wave sound)
# 13 = 10

# 14 = 1111111111111000000000000000000
# 15 = 0010110011111000110111010100001 (Buzz atonal buzz, good for percussion)

# from TIASOUND.TXT - TIA SOUND EMULATION V1.0 

 # HEX  D3 D2 D1 D0    Clock Source    Clock Modifier    Source Pattern
 # --- -------------  --------------  ----------------  ----------------
 #  0    0  0  0  0    3.58 MHz/114 ->  none  (pure)  ->      none
 #  1    0  0  0  1    3.58 MHz/114 ->  none  (pure)  ->   4-bit poly  
 #  2    0  0  1  0    3.58 MHz/114 ->  divide by 31  ->   4-bit poly
 #  3    0  0  1  1    3.58 MHz/114 ->   5-bit poly   ->   4-bit poly
 #  4    0  1  0  0    3.58 MHz/114 ->  none  (pure)  ->   pure  (~Q)
 #  5    0  1  0  1    3.58 MHz/114 ->  none  (pure)  ->   pure  (~Q)
 #  6    0  1  1  0    3.58 MHz/114 ->  divide by 31  ->   pure  (~Q)
 #  7    0  1  1  1    3.58 MHz/114 ->   5-bit poly   ->   pure  (~Q)
 #  8    1  0  0  0    3.58 MHz/114 ->  none  (pure)  ->   9-bit poly
 #  9    1  0  0  1    3.58 MHz/114 ->  none  (pure)  ->   5-bit poly
 #  A    1  0  1  0    3.58 MHz/114 ->  divide by 31  ->   5-bit poly
 #  B    1  0  1  1    3.58 MHz/114 ->   5-bit poly   ->   5-bit poly
 #  C    1  1  0  0    1.19 MHz/114 ->  none  (pure)  ->   pure  (~Q)
 #  D    1  1  0  1    1.19 MHz/114 ->  none  (pure)  ->   pure  (~Q)
 #  E    1  1  1  0    1.19 MHz/114 ->  divide by 31  ->   pure  (~Q)
 #  F    1  1  1  1    1.19 MHz/114 ->   5-bit poly   ->   pure  (~Q)

# from TiaSound.c

p4 = 0
p5 = 0
p9 = 0

Pure = [0, 1]

Div31 = [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0]

Bit5  = [0,0,1,0,1,1,0,0,1,1,1,1,1,0,0,0,1,1,0,1,1,1,0,1,0,1,0,0,0,0,1]
POLY5_SIZE = len(Bit5)

Bit4= [1,1,0,1,1,1,0,0,0,0,1,0,1,0,0]
POLY4_SIZE = len(Bit4)

Bit9 = []
POLY9_SIZE = 511
POLY9 = 0x08 

for i in range (POLY9_SIZE):
    Bit9.append(random.randint(0,1))


 # CODE DRIVER NAME    DESCRIPTION
 #  1   110    Saw     sounds similar to a saw waveform
 #  3   111    Engine  many 2600 games use this for an engine sound
 #  4   000    Square  a high pitched square waveform
 #  6   001    Bass    fat bass sound
 #  7   010    Pitfall log sound in pitfall, low and buzzy
 #  8   011    Noise   white noise
 # 12   101    Lead    lower pitch square wave sound
 # 15   100    Buzz    atonal buzz, good for percussion


p = pyaudio.PyAudio()
stream = p.open(rate=f1, channels=1, format=pyaudio.paInt8, output=True)

collision_detection = [0] * NUMBER_OF_OBJECTS
collision_array = [0] * (SCREEN_X * SCREEN_Y) 

move = ''


def sound(audv, audf, audc, length):
    """Plays a sound for slightly less than one frame rate."""
    global p4
    global p5
    global p9

    audv = (audv & 0xF) * 8
    audio_data = []
    clk_divider = 1
    if audc & 0x0C == 0x0C:
        clk_divider = 3

    div_n_cnt = clk_divider
    outvol = 0

    for i in range(length):
        if div_n_cnt > 1:
            div_n_cnt -=1
        else:
            div_n_cnt = clk_divider * audf 

            p5 += 1
            if p5 >= POLY5_SIZE:
                p5 = 0

            if (((audc & 0x02) == 0) 
                or (((audc & 0x01) == 0) and Div31[p5])
                or (((audc & 0x01) == 1) and Bit5[p5])):

                if audc & 0x04:
                    if outvol:
                       outvol = 0
                    else: 
                        outvol = audv
                elif audc & 0x08:
                    if audc == POLY9:
                        p9 += 1
                        if p9 >= POLY9_SIZE:
                            p9 = 0
                        if Bit9[p9]:
                            outvol = audv
                        else:
                            outvol = 0
                    else:
                        if Bit5[p5]:
                            outvol = audv
                        else:
                            outvol = 0
                else:
                    p4 += 1
                    if p4 >= POLY4_SIZE:
                        p4 = 0
                    if Bit4[p4]:
                        outvol = audv
                    else:
                        outvol = 0
        audio_data.append(outvol)

#    print audio_data   
    stream.write(array.array('H',audio_data).tostring())


def init_switches():
    """Set up key repeat."""
    pygame.key.set_repeat(100, 100)

def update_switches():
    """Tests returns quit, right, left, or fire."""
    move_test = ''
    event_test = pygame.event.poll()
    if event_test.type == pygame.QUIT:
        move_test = 'quit'
    if event_test.type == pygame.KEYDOWN:
        if event_test.key == K_RIGHT:
            move_test = 'right0'
        if event_test.key == K_LEFT:
            move_test = 'left0'
        if event_test.key == K_UP:
            move_test = 'up0'
        if event_test.key == K_DOWN:
            move_test = 'down0'                 
        if event_test.key == K_SPACE:
            move_test = 'fire0'
        if event_test.key == K_j:
            move_test = 'right1'
        if event_test.key == K_g:
            move_test = 'left1'
        if event_test.key == K_y:
            move_test = 'up1'
        if event_test.key == K_h:
            move_test = 'down1'                 
        if event_test.key == K_f:
            move_test = 'fire1'



    return move_test


def reset_collision():
    """Clear collisoin detection."""
    global collision_detection
    global collision_array

    collision_detection = [0] * NUMBER_OF_OBJECTS
    collision_array = [0] * (SCREEN_X * SCREEN_Y) 


def update_collision(new_object, x, y):    
    """Update array and collision registers."""
    global collision_detection
    global collision_array

    if (x >= 0 and x < SCREEN_X and y >= 0 and y < SCREEN_Y):
        collision_array[x + (y * SCREEN_X)] |= (1<<new_object)
        collision_detection[new_object] |= collision_array[x + (y * SCREEN_X)]


def test_for_object(test_object, x, y):    
    """Test to see what objects are in location."""
    global collision_array
    test_value = 0
    if (x >= 0 and x < SCREEN_X and y >= 0 and y < SCREEN_Y):
        if collision_array[x + (y * SCREEN_X)] & 1<<test_object:
            test_value = 1
    return test_value

def get_collision(first_object, second_object):
    """Performs a test between two objects (P0, M0, P1, M0, ,PF, BL)
     0 = no collision, 1 = collision."""   
    global collision_detection   
    test_value = 0

    if  (collision_detection[first_object] & 1<<second_object) > 0:
        test_value = 1

    if  (collision_detection[second_object] & 1<<first_object) > 0:
        test_value = 1

    return test_value


def game_title(name):
    """Set pygame window title."""
    pygame.display.set_caption(name)
    

def background(screen, y, height, color):
    """Background coloring, either full screen or sections."""
    if height == WINDOWHEIGHT:
        screen.fill(color) 
    else:
        for i in range(height):       
            pygame.draw.line(screen, color
                , (0, (y + i) * PIXEL)
                ,(WINDOWWIDTH, (y + i) * PIXEL)
                , PIXEL)


def playfield_collision(x, y):
    """Prints a 3x5 digit using Playfield pixels"""
    update_collision(PF, x, y)
    update_collision(PF, x + 1, y)
    update_collision(PF, x + 2, y)
    update_collision(PF, x + 3, y)    


def place_digit(screen, x, y, digit, color):
    """Prints a 3x5 digit using Playfield pixels"""
    for j in range(5):
        k = digits[(digit * 5) + j]
        for i in range(3):
            if k[i] == 'X':
                pygame.draw.line(screen, color
                    , ((x+i)*PF_PIXEL, ((y +j) * PIXEL))
                    , ((x+i)*PF_PIXEL + PF_PIXEL, ((y +j) * PIXEL))
                    , PIXEL)
                playfield_collision((x+i)*4, y + j)


def number(screen, x, y, value, color):
    """Prints a numeric value that is right justified using 3x5 digits in 
    Playfield pixels."""
    if value < 0:
        value -= value
    value_string = str(value)
    for i in range(len(value_string)):
        j = int(value_string[len(value_string) - 1 - i])
        place_digit(screen, x - (i*4), y, j, color)

def playfield(screen, y, height, data, color, left, right):
    """Playfield drawing and collision detection."""
    if left == 2:
        for j in range(height): 
            for i in range(20):
                if data[i] == 'X':       
                    pygame.draw.line(screen, color
                        , (WINDOWWIDTH/2 - (i*PF_PIXEL), ((y +j) * PIXEL))
                        , (WINDOWWIDTH/2 - (i*PF_PIXEL) - PF_PIXEL
                        , ((y +j) * PIXEL)), PIXEL)
                    playfield_collision(SCREEN_X/2 - (i*4) - 4, y + j)

    if left == 1:
        for j in range(height): 
            for i in range(20):
                if data[i] == 'X':       
                    pygame.draw.line(screen, color
                        , ((i*PF_PIXEL), ((y +j) * PIXEL))
                        , ((i*PF_PIXEL) + PF_PIXEL, ((y +j) * PIXEL)), PIXEL)
                    playfield_collision(i*4, y + j)

    if right == 2:
        for j in range(height): 
            for i in range(20):
                if data[i] == 'X':       
                    pygame.draw.line(screen, color
                        , (WINDOWWIDTH - (i*PF_PIXEL), ((y +j) * PIXEL))
                        , (WINDOWWIDTH - (i*PF_PIXEL) - PF_PIXEL
                        , ((y +j) * PIXEL)), PIXEL)
                    playfield_collision(SCREEN_X - (i*4) - 4, y + j)

    if right == 1:
        for j in range(height): 
            for i in range(20):
                if data[i] == 'X':       
                    pygame.draw.line(screen, color
                        , (WINDOWWIDTH/2 + (i*PF_PIXEL), ((y +j) * PIXEL))
                        , (WINDOWWIDTH/2 + (i*PF_PIXEL) + PF_PIXEL
                            , ((y +j) * PIXEL)), PIXEL)
                    playfield_collision(SCREEN_X/2 + (i*4), y + j)



def ball(screen, x, y, width, height, color):
    """Ball drawing and collision detection."""
    for i in range(height):       
        pygame.draw.line(screen, color
            , ((x * PIXEL), (y + i) * PIXEL)
            ,((x * PIXEL) + (width * PIXEL), (y + i) * PIXEL)
            , PIXEL)
        for j in range(width):
            update_collision(BL, x + j, y + i)


def missile0(screen, x, y, width, height, color):
    """Missile0 drawing and collision detection."""
    for i in range(height):       
        pygame.draw.line(screen, color
            , ((x * PIXEL), (y + i) * PIXEL)
            ,((x * PIXEL) + (width * PIXEL), (y + i) * PIXEL)
            , PIXEL)
        for j in range(width):
            update_collision(M0, x + j, y + i)


def missile1(screen, x, y, width, height, color):
    """Missile1 drawing and collision detection."""
    for i in range(height):       
        pygame.draw.line(screen, color
            , ((x * PIXEL), (y + i) * PIXEL)
            ,((x * PIXEL) + (width * PIXEL), (y + i) * PIXEL)
            , PIXEL)
        for j in range(width):
            update_collision(M1, x + j, y + i)


def player0(screen, x, y, data, color):
    """Player0 drawing and collision detection."""
    for j in range(len(data)):
        k = data[j]
        for i in range(8):
            if k[i] == 'X':
                pygame.draw.line(screen, color, 
                ((x + i)*PIXEL,(y + j)*PIXEL)
                , (((x + i)*PIXEL + PIXEL),(y + j)*PIXEL), PIXEL)
                update_collision(P0, x + i, y + j)


def player1(screen, x, y, data, color):
    """Player1 drawing and collision detection."""
    for j in range(len(data)):
        k = data[j]
        for i in range(8):
            if k[i] == 'X':
                pygame.draw.line(screen, color, 
                ((x + i)*PIXEL,(y + j)*PIXEL)
                , (((x + i)*PIXEL + PIXEL),(y + j)*PIXEL), PIXEL)
                update_collision(P1, x + i, y + j)


screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()
reset_collision()
init_switches()
