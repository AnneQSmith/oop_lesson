import core
import pyglet
import random
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 9
GAME_HEIGHT = 12

#### Put class definitions here ####
class Obstacle (GameElement):
    IMAGE = 'Rock'
    SOLID = True

class Character(GameElement):
    IMAGE = "Horns"

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = 25*['E']

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
    # total= ((GAME_HEIGHT-2)* (GAME_WIDTH))/3

    # x_range = range(0, GAME_WIDTH)
    # y_range = range(1, GAME_HEIGHT-1)

    # for obs in range(total):
    #     x_coor = random.choice(x_range)
    #     y_coor = random.choice(y_range)
    #     obstacle_positions[obs] = (x_coor, y_coor)

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

    energyBar = EnergyBar()
    GAME_BOARD.register(energyBar)
    GAME_BOARD.set_el(6, 9, energyBar)







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

          
        if len(PLAYER.inventory) >= 1:
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


        else:
            GAME_BOARD.draw_msg("You have no energy left; you fall to your death")
            


