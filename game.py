import core
import pyglet
import random
from pyglet.window import key
from core import GameElement
import sys
import time

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 9
GAME_HEIGHT = 12
INITIAL_DELAY = .5

#### Put class definitions here ####
class Obstacle (GameElement):
    IMAGE = 'Rock'
    SOLID = True


class Corpse(GameElement):
    IMAGE = "Bug"


class Character(GameElement):
    IMAGE = "Horns"

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = 10*['E']
        self.counter = 0
        self.accel = 1

    def update(self, dt):
        # if inventory is empty
        #    fall

 

        if len(self.inventory) == 0:
            #fall!
            # if time to draw frame
            self.counter +=1
            if self.y < GAME_HEIGHT-1 and self.counter % (30/self.accel) == 0:
                self.accel +=1
                self.counter = 1
                GAME_BOARD.del_el(self.x, self.y)
                self.y += 1
                if self.y == GAME_HEIGHT-1:
                    corpse = Corpse()
                    GAME_BOARD.del_el(self.x, self.y)
                    GAME_BOARD.register(corpse)
                    GAME_BOARD.set_el(self.x,GAME_HEIGHT-1,corpse)    
                else:
                    GAME_BOARD.set_el(self.x, self.y, self)

# def update(dt):
#     for el in update_list:
#         el.update(dt)




    def next_pos(self, direction):

        if direction == 'up':
            return (self.x, max(self.y-1,0))
        elif direction == "down":
            return (self.x, min(self.y+1, GAME_HEIGHT-1))
        elif direction == 'left':
            return (max (0, self.x-1), self.y)
        elif direction=='right':
            return (min (self.x+1, GAME_WIDTH-1), self.y)
        return None



class EnergyBar (GameElement):
    IMAGE = "BlueGem"
    SOLID = False

    def interact(self, player):
#TODO fix this
        player.inventory.append(self)
        player.inventory.append(self)
        player.inventory.append(self)
        GAME_BOARD.draw_msg(("You just ate an energy bar! You have %r units of energy left!") % (len(player.inventory)))


####   End class definitions    ####

def initialize():
    """Put game initialization code here"""

   # obstacle_positions = [(3,1), (1,2), (3, 2), (2, 4)]

    obstacle_positions =[]

    #  THIS BELOW NEEDS SORTING OUT
    total= ((GAME_HEIGHT-2)* (GAME_WIDTH))/3

    x_range = range(0, GAME_WIDTH)
    y_range = range(1, GAME_HEIGHT-1)


    for obs in range(total):

        x_coor = random.choice(x_range)
        y_coor = random.choice(y_range)

       # print obs, x_coor, y_coor
        obstacle_positions.append((x_coor, y_coor))

    obstacles=[]
    for pos in obstacle_positions:
        obstacle = Obstacle()

        GAME_BOARD.register(obstacle)
        GAME_BOARD.set_el(pos[0], pos[1], obstacle)
        obstacles.append(obstacle)

    for obstacle in obstacles:
        print obstacle 

    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(4, 11, PLAYER)
    print PLAYER


    GAME_BOARD.draw_msg("This game is wicked awesome.")

    
    energyBar_positions = []

    total = 5

    for i in range(total):
        if i%2 ==0:
            y_range = range(GAME_HEIGHT/2, GAME_HEIGHT-1)
        
        else:
            y_range = range(1, GAME_HEIGHT/2)

        x_coor = random.choice(x_range)
        y_coor = random.choice(y_range)  
        energyBar_positions.append((x_coor, y_coor))

    energyBars =[]
    for position in energyBar_positions:
        energyBar = EnergyBar()
        GAME_BOARD.register(energyBar)
        GAME_BOARD.set_el(position[0], position[1], energyBar)
        energyBars.append(energyBar)



def keyboard_handler():

    direction = None

    if KEYBOARD[key.UP]:
        direction = 'up'

    elif KEYBOARD[key.DOWN]:
        direction = 'down'

    elif KEYBOARD[key.RIGHT]:
        direction = 'right'

    elif KEYBOARD[key.LEFT]:
        direction = 'left'

    elif KEYBOARD[key.QUESTION]:
        GAME_BOARD.draw_msg("Sorry you are beyond help")
    elif KEYBOARD[key.SPACE]:
        GAME_BOARD.erase_msg()


    if direction:

        if len(PLAYER.inventory) ==  0:
            GAME_BOARD.draw_msg("You have no energy left; you fall to your death")
            print "We should be in a death spiral"
            print "player.y, game height-1",PLAYER.y,GAME_HEIGHT-1
       
      
    
        else:
            PLAYER.inventory.pop()
        
            GAME_BOARD.draw_msg("You only have %d units of energy left" % (len(PLAYER.inventory)))
            next_location = PLAYER.next_pos(direction)
            next_x = next_location[0]
            next_y = next_location[1]

            existing_el = GAME_BOARD.get_el(next_x,next_y)

            if existing_el:
                existing_el.interact(PLAYER)


            if existing_el is None or not existing_el.SOLID:

                GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
                GAME_BOARD.set_el(next_x, next_y, PLAYER)

                if next_y == 0:
                    GAME_BOARD.draw_msg("YOU GOT TO THE SUMMIT!")



            # fall_location = (PLAYER.x, PLAYER.y)   

            # def dummycallback(dt):
            #     print '%f seconds since the last time' % dt   
               
            #     print "in dummy", PLAYER.x, PLAYER.y

            #     if PLAYER.y < GAME_HEIGHT - 1:
            #         GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            #         GAME_BOARD.set_el(PLAYER.x, PLAYER.y+1, PLAYER)
            #         return
            #     else:
            #         pyglet.clock.unschedule(dummycallback)
            #         return

            
# loop over remaining fall:
            # while (PLAYER.y < GAME_HEIGHT-1):
            # pyglet.clock.schedule_interval(dummycallback, INITIAL_DELAY)
            
            # def fall(dt,fall_location):
            #     # for i in range (fall_location[1], GAME_HEIGHT-1):
            #     #     print i
                # while (PLAYER.y < GAME_HEIGHT-1):
                #     print "in fall i ",i
                #     print PLAYER.x, PLAYER.y
                #     GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
                #     GAME_BOARD.set_el(PLAYER.x, PLAYER.y+1, PLAYER)    
                # return 

            # for i in range (fall_location[1], GAME_HEIGHT-2):
            #     print "in range i = ",i
            #     print PLAYER.x, PLAYER.y
            #     pyglet.clock.schedule_interval(fall, 1, fall_location=(PLAYER.x,PLAYER.y))
           


