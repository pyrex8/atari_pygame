#! /usr/bin/env python
""" atari 2600 Combat functionality to test atari.py functionality""" 

__author__ = "Rex Allison"
__copyright__ = "Copyright 2016, Rex Allison"
__license__ = "MIT"

from atari import *
import math 

MOVE_UPDATE_RATE = 5

# all playfeild and player data here
color0 = 0
sound_number = 0
freq_number = 0
sound_on = 0

move_update = 0

score0 = 0
tank0_hit = 0
tank0_angle = 0
tank0_x = 40
tank0_y = SCREEN_Y/2 - 4

score1 = 0
tank1_hit = 0
tank1_angle = 8
tank1_x = SCREEN_X/2 - 8 #SCREEN_X - 18
tank1_y = SCREEN_Y/2 - 4

fire0_busy = 0 
fire0_angle = 0
fire0_x = 0
fire0_y = 0

fire1_busy = 0 
fire1_angle = 0
fire1_x = SCREEN_X - 10
fire1_y = SCREEN_Y/2

move_table_x = [2,2,2,1,0,-1,-2,-2,-2,-2,-2,-1,0,1,2,2]
move_table_y = [0,-1,-2,-2,-2,-2,-2,-1,0,1,2,2,2,2,2,1]

# ; Table of color combinations.  Each 4 byte entry specifies
# ; Player 0, Player1, Playfield, and Background colors.
# ; (By a not-so-odd coincidence, these 4 color registers are
# ; addressed consecutively in the same order in the TIA.)
# ; Table is indexed by the high 2 bits of GAMVAR << 2, or
# ; forced to +$10 if B&W switch selected.
# ;
# ColorTbl
#     byte $EA ,$3C ,$82 ,$44      ; 00 = Regular Tanks
#        .byte $32 ,$2C ,$8A ,$DA      ; 01 = Tank Pong
#        .byte $80 ,$9C ,$DA ,$3A      ; 10 = Jets
#        .byte $64 ,$A8 ,$DA ,$4A      ; 11 = Biplanes
#        .byte $08 ,$04 ,$00 ,$0E      ; special B&W

# P0 = red = 33
color_p0 = 68/2 #68 //33
color_p1 = 130/2 #130 // 65
color_pf = 60/2 #60 // 22
color_bk = 234/2 #234 // 11



tank = []

tank =  ['        '
        ,'XXXXXX  '
        ,'XXXXXX  '
        ,'  XXX   '
        ,'  XXXXXX'
        ,'  XXX   '
        ,'XXXXXX  '
        ,'XXXXXX  '

        ,'   XXX  '
        ,' XXXX   '
        ,'XXXXX XX'
        ,'XXXXX   '
        ,'   XXX  '
        ,'   XXXXX'
        ,'  XXXXX '
        ,'   XX   '

        ,'   XX  X'
        ,'  XXX X '
        ,' XXXXX  '
        ,'XXXXXXXX'
        ,'XX XXXXX'
        ,'    XXX '
        ,'   XXX  '
        ,'   XX   '
       
        ,'  X  X  '
        ,' XX  X  '
        ,' XXXX  X'
        ,'XXXXXXXX'
        ,'XXXXXXXX'
        ,' X  XXX '
        ,'    XXX '
        ,'     X  '

        ,'    X   '
        ,'    X   '
        ,' XX X XX'
        ,' XXXXXXX'
        ,' XXXXXXX'
        ,' XXXXXXX'
        ,' XX   XX'
        ,' XX   XX']
       

for j in range(4):
    for i in range(8):
        tank.append(tank[(3-j)*8+i][::-1])

for j in range(8):
    for i in range(8):
        tank.append(tank[(7-j)*8+(7-i)])


            # 01234567890123456789
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
            ,'X.....X...XX........'
            ]
# end data
game_title('combat')
move = ''

while move != 'quit':
    reset_collision()
    background(screen, 0, WINDOWHEIGHT, colors_hex[color_bk])

    # Game code starts here

    # update graphics here

    if move == 'left0':
        tank0_angle += 1
        freq_number = (freq_number - 1) & 0x1F
        print freq_number             
        
#        sound (20)
    if move == 'right0':
        tank0_angle -= 1
#        sound (10)   
        freq_number = (freq_number + 1) & 0x1F
        print freq_number             
    tank0_angle &= 0x0F

    if move == 'up0':
        tank0_x += move_table_x[tank0_angle]
        tank0_y += move_table_y[tank0_angle]
        sound_number = (sound_number + 1) & 0xF
        print sound_number 

    if move == 'down0':
        sound_number = (sound_number - 1) & 0xF
        print sound_number 




    if move == 'fire0':
        if sound_on == 1:
            sound_on = 0
        else:
            sound_on = 1
        if fire0_busy == 0 and tank1_hit == 0:
            fire0_x = tank0_x + 4
            fire0_y = tank0_y + 4
            fire0_angle = tank0_angle
            fire0_busy = 50
            

    if move == 'left1':
        tank1_angle += 1
        
#        sound (20)
    if move == 'right1':
        tank1_angle -= 1
#        sound (10)       
    tank1_angle &= 0x0F

    if move == 'up1':
        tank1_x += move_table_x[tank1_angle]
        tank1_y += move_table_y[tank1_angle]
#        sound (5) 

    if move == 'fire1':
        if fire1_busy == 0 and tank0_hit == 0:
            fire1_x = tank1_x + 4
            fire1_y = tank1_y + 4
            fire1_angle = tank1_angle
            fire1_busy = 50
#            sound (15)
            print samples


    if sound_on == 1:
        sound (8, freq_number, sound_number, 1000)    



     # spin tanks if hit
    if tank0_hit > 0:
        tank0_hit -= 1
        tank0_angle += 1

    if tank1_hit > 0:
        tank1_hit -= 1
        tank1_angle += 1

    # put tanks back in visiable playfield 
    if tank0_x > SCREEN_X - 10:
        tank0_x = 10
    if tank0_x < 10:
        tank0_x = SCREEN_X - 10    

    if tank0_y > SCREEN_Y - 10:
        tank0_y = 10
    if tank0_y < 10:
        tank0_y = SCREEN_Y - 10

    if tank1_x > SCREEN_X - 10:
        tank1_x = 10
    if tank1_x < 10:
        tank1_x = SCREEN_X -10    

    if tank1_y > SCREEN_Y - 10:
        tank1_y = 10
    if tank1_y < 10:
        tank1_y = SCREEN_Y - 10


    if fire0_busy > 0 and tank1_hit == 0:
        fire0_busy -= 1
        fire0_x += move_table_x[fire0_angle]
        fire0_y += move_table_y[fire0_angle]
        missile0(screen, fire0_x + 4, fire0_y + 4, 1, 1, colors_hex[color_p0])

    if fire1_busy > 0 and tank0_hit == 0:
        fire1_busy -= 1
        fire1_x += move_table_x[fire1_angle]
        fire1_y += move_table_y[fire1_angle]
        missile1(screen, fire1_x + 4, fire1_y + 4, 1, 1, colors_hex[color_p1])
    # missile0(screen, x, y, width, height, color)
    
    # player0(screen, x, y, data, color)
    player0(screen, tank0_x + 4, tank0_y + 4
        , tank[tank0_angle*8:tank0_angle*8+8], colors_hex[color_p0])

    player1(screen, tank1_x + 4, tank1_y + 4
        , tank[tank1_angle*8:tank1_angle*8+8], colors_hex[color_p1])

    # playfield.playfield(screen, y, data, color, left, right)
    for i in range(len(pfield)):
        playfield(screen, 8 + i*4, 4, pfield[i], colors_hex[color_pf], 1, 2)
        playfield(screen, 8 + 4*23 - i*4, 4, pfield[i], colors_hex[color_pf]
            , 1, 2)

    number(screen, 10, 2, score0, colors_hex[color_p0])
    number(screen, 30, 2, score1, colors_hex[color_p1])

    move = update_switches()

    if get_collision(P0, PF):
        tank0_x += 2*move_table_x[(tank0_angle + 8) & 0x0F]
        tank0_y += 2*move_table_y[(tank0_angle + 8) & 0x0F]

    if get_collision(P1, PF):
        tank1_x += 2*move_table_x[(tank1_angle + 8) & 0x0F]
        tank1_y += 2*move_table_y[(tank1_angle + 8) & 0x0F]

    if get_collision(P0, P1):
        tank0_x += 2*move_table_x[(tank0_angle + 8) & 0x0F]
        tank0_y += 2*move_table_y[(tank0_angle + 8) & 0x0F]
        tank1_x += 2*move_table_x[(tank1_angle + 8) & 0x0F]
        tank1_y += 2*move_table_y[(tank1_angle + 8) & 0x0F]

    if get_collision(P0, M1):
        score1 += 1
        tank0_hit = 10
        tank0_angle = fire1_angle
        tank0_x += 4*move_table_x[(tank0_angle + 8) & 0x0F]
        tank0_y += 4*move_table_y[(tank0_angle + 8) & 0x0F]

    if get_collision(P1, M0):
        score0 += 1
        tank1_hit = 10
        tank1_angle = fire0_angle
        tank1_x += 4*move_table_x[(tank1_angle + 8) & 0x0F]
        tank1_y += 4*move_table_y[(tank1_angle + 8) & 0x0F]

    if get_collision(M0, PF):
        fire0_busy = 0

    if get_collision(M1, PF):
        fire0_busy = 0

    # Game code ends here
    pygame.display.flip()
    clock.tick(FRAME_RATE)

stream.close()
p.terminate()    
pygame.quit()





