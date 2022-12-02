import pygame
from constants import *
import random

# define a class for a layer of pegs, and may contain reflectors
class PegLayer:
    def __init__(self, y, pegnos, lIndex, board):
        self.y = y
        self.lIndex = lIndex
        self.pegnos = pegnos
        self.pegs = []
        self.board = board
        # the pegs shall be centered on the screen
        # pegs are staggered across each layer
        # in the shape of a triangle
        # the middle peg is centered on the screen
        # each peg is 100 pixels apart from the next
        for i in range(0, pegnos):
            x = 550 - (pegnos - 1) * 50 + i * 100
            self.pegs.append(Peg(x, y, lIndex, i))

    def draw(self):
        for peg in self.pegs:
            peg.draw()


# define a slotlayer class inheriting from the peglayer class
class SlotLayer (PegLayer):
    def __init__(self, y, pegnos, lIndex, board):
        self.y = y
        self.lIndex = lIndex
        self.pegnos = pegnos
        self.pegs = []
        self.board = board
        # There are 11 slots at the bottom of the board
        # The slots shall be numbered 1,2,3,4,0,5,6,7,8, with a placeholder slot on the left and right of the board
        # The slot at the leftmost side is 1, the slot at the rightmost side is 8
        # The slot in the middle is 0
        # The slots alternate between black and red in color except for the middle slot which is always white
        # the slots are centered on the screen
        # the slots are 100 pixels wide and 100 pixels high
        slots = []
        for i in range(11):
            x = 500 - (11 - 1) * 50 + i * 100
            slots.append(Slot(x, y, slotsinfo[i][1], slotsinfo[i][0], lIndex, i))
        self.slots = slots
        self.pegs = slots

    def draw(self):
        for peg in self.pegs:
            peg.draw()

# Define pegs, balls, slots, and score
class Peg:
    def __init__(self, x, y, lIndex, index):
        self.x = x
        self.y = y
        self.lIndex = lIndex
        self.index = index
        self.color = (255, 255, 255)
        self.radius = 10
        self.type = "peg"

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

# the ball starts at the top of the board and can be moved left or right above any peg in the top layer by the user using the left and right arrow keys
# the ball falls down the board and must hit a peg in each layer and go left or right randomly
# the ball lands in one of the slots at the bottom of the board
# there are 9 slots numbered 1,2,3,4,0,5,6,7,8 from left to right

# there is a reflector on the bottom left and bottom right of the board that forces the ball to go right or left respectively into the slots 1 and 8

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # ball is yellow
        self.color = (255, 255, 0)
        self.radius = 10
        self.gravity = 1
        self.downwardspeed = 0
        self.direction = 0

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
    
# inherits from the Peg class
class Slot (Peg):
    def __init__(self, x, y, color, text, lIndex, index):
        self.x = x
        self.y = y
        self.color = color
        # there are 9 slots which cover the width of the bottom of the board
        self.width = 100
        self.height = 100
        self.text = text
        self.lIndex = lIndex
        self.index = index
        self.type = "slot"


    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.Font(None, 36)
        # the text colour is automatically contrasted with the slot colour
        if self.color == (255, 255, 255):
            textcolor = (0, 0, 0)
        else:
            textcolor = (255, 255, 255)
        text = font.render(self.text, 1, textcolor)
        textpos = text.get_rect()
        textpos.centerx = self.x + self.width/2
        textpos.centery = self.y + self.height/2
        # slots are outlined on left and right side using dark grey lines
        pygame.draw.line(screen, (50, 50, 50), (self.x, self.y), (self.x, self.y + self.height), 5)
        screen.blit(text, textpos)

screen = pygame.display.set_mode(size)





# a reflector forces the ball to go the direction the reflector is pointing, it looks like this:
# a reflector looks like a slanted line
class Reflector:
    def __init__(self, x, y, direction, lIndex, index):
        self.x = x
        self.y = y
        self.direction = direction
        self.color = (255, 255, 255)
        self.width = 100
        self.height = 100
        self.type = "reflector"
        self.lIndex = lIndex
        self.index = index
    
    def draw(self):
        if self.direction == 1:
            pygame.draw.line(screen, self.color, (self.x, self.y), (self.x + self.width, self.y + self.height), 10)
        else:
            pygame.draw.line(screen, self.color, (self.x, self.y + self.height), (self.x + self.width, self.y), 10)