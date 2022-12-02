# Import pygame, plinko, betting, objects and constants
import os
import pygame
import plinko
import betting
import scoreboard
import sys
import objects
import json
from constants import *
# Initialise the game engine
pygame.init()
# loop
# state machine
# 0 bettingscreen
# 1 plinkoscreen
# 2 scoreboardscreen
screen = pygame.display.set_mode(size)
# set the title of the window
pygame.display.set_caption("Pascal's Painful Plinko")
turn = 1
# create a clock
clock = pygame.time.Clock()
# create a board
board = plinko.Board()
# create a layout
layout = betting.Layout()
# create a scoreboard
scoreboard = scoreboard.Scoreboard()
# set the state to the bettingscreen
state = 0
# loop
layout.score = 3
font = pygame.font.SysFont("Arial", 20)
outcomes = {"0":0,"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"8":0}
while True:
    if state == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                layout.placebet(*(pygame.mouse.get_pos()))
            # if enter is pressed and the state is the bettingscreen then change the state to the plinkoscreen
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and state == 0:
                    state = 1
        screen.fill(black)
        layout.draw()
    elif state == 1:
        board.ball.x = 1000
        board.ball.y = 50
        for event in pygame.event.get():
            # if the user clicks the close button, stop the game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
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
                    result = slotsinfo[board.dropball()]
                    # load the json file outcomes
                    # check if outcomes.json exists
                    if os.path.exists("outcomes.json"):
                        with open("outcomes.json", "r") as f:
                            outcomes = json.load(f)
                    # add the result to the outcomes
                    outcomes[result[0]] += 1
                    with open("outcomes.json", "w") as f:
                        json.dump(outcomes, f)
                    layout.result(result[1], int(result[0]))
                    turn += 1
                    if turn > 10:
                        screen = pygame.display.get_surface()
                        screen.fill(white)
                        font = pygame.font.SysFont("Arial", 30)
                        text = font.render("Your score is: " + str(layout.score), True, black)
                        # center the text middle x axis, 1/4 y axis
                        centerx = (screen.get_width() / 2) - (text.get_width() / 2)
                        centery = (screen.get_height() / 4) - (text.get_height() / 2)
                        screen.blit(text, (centerx, centery))
                        text1 = font.render("Press enter to continue", True, black)
                        # bottom right of the screen, right aligned
                        screen.blit(text1, (screen.get_width() - text1.get_width(), screen.get_height() - text1.get_height()))
                        flag = True
                        while flag:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_RETURN:
                                        flag = False
                            pygame.display.update()
                        scoreboard.add(layout.score)
                        state = 2
                        continue
                    else:
                        state = 0
                    layout.score += 3

        # draw the board
        board.draw()
        # update the display
    elif state == 2:
        # add the score to the scoreboard
        # draw the scoreboard
        scoreboard.draw()
        # if the user presses the return key, reset the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    state = 0
                    turn = 1
                    layout.score = 3
        screen.fill(black)
        scoreboard.draw()
    # display turn number
    # terrible code, please do not replicate
    if state != 2:
        font = pygame.font.SysFont("Arial", 30)
        text = font.render("Turn: " + str(turn), True, white)
        screen.blit(text, (50, 0))
        pygame.display.update()
    clock.tick(60)


