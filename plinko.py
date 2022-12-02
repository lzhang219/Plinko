# Simple plinko board implemented in python pygame
# Path: plinko.py

# Import submodules
from constants import *
from objects import *
# Import the pygame library and initialise the game engine
import pygame
import random
# import necessary pygame submodules
from pygame.locals import *
import pygame.time

        
# define a board class containing all the pegs, slots, and a ball
class Board:
    def __init__(self):
        self.peglayers = []
        for i in range(8):
            self.peglayers.append(PegLayer(100 + (i * 40), pegnos[i], i, self))
        self.ball = Ball(400, 50)
        # There are 9 slots at the bottom of the board
        # The slots shall be numbered 1,2,3,4,0,5,6,7,8
        # The slot at the leftmost side is 1, the slot at the rightmost side is 8
        # The slot in the middle is 0
        # The slots alternate between black and red in color except for the middle slot which is always white
        # the slots are centered on the screen
        # the slots are 100 pixels wide and 100 pixels high
        slots = SlotLayer(500, 11, 8, self)
        self.peglayers.append(slots)
        self.slots = slots
        self.dropped = False
        # there are 2 reflectors on the bottom of the board
        # the reflector on the left forces the ball to go right
        # the reflector on the right forces the ball to go left
        self.peglayers[7].pegs.insert(0, Reflector(0, 400, 1, 7, 0))
        self.peglayers[7].pegs.append(Reflector(1000, 400, -1, 7, 1))
        for index, pegs in enumerate(self.peglayers[7].pegs):
            pegs.index = index

        # select the top middle peg as the starting peg
        self.selectedpeg = self.peglayers[0].pegs[pegnos[0] // 2]

    def draw(self):
        # board is green
        screen.fill((0, 127, 0))
        for layer in self.peglayers:
            layer.draw()
        self.ball.draw()
        if not self.dropped:
            font = pygame.font.SysFont("Arial", 30)
            text = font.render("Press space to drop the ball", True, (255, 255, 255))
            screen.blit(text, (15, 30))
        # highlight the selected peg
        pygame.draw.circle(screen, (255, 0, 0), (self.selectedpeg.x, self.selectedpeg.y), self.selectedpeg.radius)
    # define a function for the user to change the selected peg
    def selectpeg(self, direction):
        # unhighlight the selected peg
        pygame.draw.circle(screen, (0, 0, 0), (self.selectedpeg.x, self.selectedpeg.y), self.selectedpeg.radius)
        # get the index of the selected peg
        index = self.selectedpeg.index
        # get the layer of the selected peg
        layer = self.selectedpeg.lIndex
        # get the number of pegs in the layer
        pegnos = len(self.peglayers[layer].pegs)
        # if the direction is 1, the user wants to select the peg to the right
        if direction == 1:
            # if the index is the last peg in the layer, select the first peg in the layer
            if index == pegnos - 1:
                self.selectedpeg = self.peglayers[layer].pegs[0]
            # otherwise select the peg to the right
            else:
                self.selectedpeg = self.peglayers[layer].pegs[index + 1]
        # if the direction is -1, the user wants to select the peg to the left
        elif direction == -1:
            # if the index is the first peg in the layer, select the last peg in the layer
            if index == 0:
                self.selectedpeg = self.peglayers[layer].pegs[pegnos - 1]
            # otherwise select the peg to the left
            else:
                self.selectedpeg = self.peglayers[layer].pegs[index - 1]
        # check if the user is trying to select a peg that doesn't exist
        # highlight the selected peg
        pygame.draw.circle(screen, (255, 0, 0), (self.selectedpeg.x, self.selectedpeg.y), self.selectedpeg.radius)
    # define a function to move the ball above the selected peg

    def moveball(self, peg):
        # render the ball above the given object
        # if the object is a peg, move the ball above the peg
        if peg.type == "peg":
            self.ball.x = peg.x
            self.ball.y = peg.y - peg.radius - self.ball.radius
        # if the object is a slot, move the ball above the slot
        elif peg.type == "slot":
            # render the ball in the middle of the slot
            self.ball.x = peg.x + peg.width // 2
            self.ball.y = peg.y - self.ball.radius
        # if the object is a reflector, move the ball above the reflector
        elif peg.type == "reflector":
            # render the ball in the middle of the reflector
            self.ball.x = peg.x + peg.width // 2 - self.ball.radius
            self.ball.y = peg.y + 53 - self.ball.radius
    
    # drop the ball from the peg it is above and allow it to fall to a peg in the layer below or a slot if it is in the bottom layer

    # drop the ball
    def dropball(self):
        self.dropped = True
        # keep track of what the ball is above
        above = self.selectedpeg
        self.moveball(above)
        # loop until the ball reaches a slot
        tickselapsed = 0
        while True:
            tickselapsed += 1
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # every 15 ticks, move the ball
            if tickselapsed % 30 == 0:
                # check if the ball is on a peg
                if above.type == "peg":
                    # get the layer of the peg
                    layer = above.lIndex
                    # get the index of the peg
                    index = above.index
                    # randomly select a direction for the ball to move
                    direction = random.choice([-1, 1])
                    # get new index
                    if direction == 1:
                        newindex = index + 1
                    else:
                        # since it is staggered, the index remains the same if the ball is moving left
                        newindex = index 
                    # get the new peg
                    newpeg = self.peglayers[layer + 1].pegs[newindex]
                    # put the ball above the new peg
                    above = newpeg
                    self.moveball(newpeg)
                # check if the ball is on a slot
                elif above.type == "slot":
                    # end the loop
                    self.dropped = False
                    return above.index
                # check if the ball is on a reflector
                elif above.type == "reflector":
                    # get the layer of the reflector
                    layer = above.lIndex
                    # get the index of the reflector
                    index = above.index
                    # get the new index
                    if above.direction == 1:
                        newindex = index + 1
                    else:
                        newindex = index
                    # get the new peg
                    newpeg = self.peglayers[layer + 1].pegs[newindex]
                    # put the ball above the new peg
                    above = newpeg
                    self.moveball(newpeg)
            # draw the updated parts of the screen
            self.draw()
            # update the screen
            pygame.display.update()
            # set the frame rate
            clock.tick(60)
            
clock = pygame.time.Clock()
# terrible code smh, who wrote this? oh wait, that's me.
if __name__ == "__main__":   
    # main program
    # create a board
    pygame.init()
    board = Board()
    # create a clock
    running = True
    while running:
        # check for events
        for event in pygame.event.get():
            # if the user clicks the close button, stop the game
            if event.type == pygame.QUIT:
                running = False
            # if the user presses a key
            if event.type == pygame.KEYDOWN:
                # if the user presses the left arrow key, select the peg to the left
                if event.key == pygame.K_LEFT:
                    board.selectpeg(-1)
                # if the user presses the right arrow key, select the peg to the right
                if event.key == pygame.K_RIGHT:
                    board.selectpeg(1)
                # if the user presses the space bar, move the ball above the selected peg
                if event.key == pygame.K_SPACE:
                    board.dropball()
                # if the user presses the return key, drop the ball
                if event.key == pygame.K_RETURN:
                    board.dropball()
        # draw the board
        board.draw()
        # update the display
        pygame.display.update()
        # set the background color
        screen.fill((0, 0, 0))
        # set the frame rate
        # clock.tick(60)