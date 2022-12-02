import pygame
import uuid
from constants import *
import os
import json

class Scoreboard:
    def __init__(self):
        self.scores = []
        self.load()
        self.currentUserRank = 0
    # I LOVE COPYING CODE!
    def load(self):
        # load the scores from the scores file
        # check if the file exists
        if os.path.exists("scores.json"):  
            with open("scores.json", "r") as f:
                self.scores = json.load(f)
    def save(self):
        # sort the scores
        self.sort()
        # save the scores to the scores file
        with open("scores.json", "w") as f:
            json.dump(self.scores, f)
    def add(self, score):
        # add a score to the list by accepting a name via the keyboard by prompting the user to enter a name using pygame
        screen = pygame.display.get_surface()
        # set the background color
        screen.fill((0, 0, 0))
        # set the font
        font = pygame.font.SysFont("Arial", 50)
        # prompt the user to enter a name
        name = ""
        continueloop = True
        while continueloop:
            text = font.render("Enter your name:", True, white)
            # draw the text centered on screen in x and a quarter of the way down in y
            centerx = (screen.get_width() - text.get_width()) / 2
            centery = (screen.get_height() - text.get_height()) / 4
            screen.blit(text, (centerx, centery))
            # create a text box in black with a white border and green text to accept the name
            # cant figure out how to specify border color so I'll draw 2 rectangles
            pygame.draw.rect(screen, black, (centerx, centery + 100, 500, 100))
            pygame.draw.rect(screen, white, (centerx - 5, centery + 95, 510, 110), 5)
            # draw the name
            textboxfont = pygame.font.SysFont("Arial", 100)
            text = textboxfont.render(name, True, green)
            screen.blit(text, (centerx, centery + 100))
            # input the name
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # don't continue loop
                        continueloop = False
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode
            pygame.display.update()
        # generate a unique id for the score
        id = len(self.scores)
        self.scores.append((id, name, score))
        self.save()
        # find the rank of the current user
        self.currentUserRank = 0
        for i in range(len(self.scores)):
            if self.scores[i][0] == id:
                self.currentUserRank = i + 1
                break
        

    def sort(self):
        # sort the scores if there are more than 1
        if len(self.scores) > 1:
            self.scores.sort(key=lambda x: int(x[2]), reverse=True)
    def draw(self):
        # sort the scores
        self.sort()
        # display 10 scores with the highest score at the top of the screen
        # name is left aligned and score is right aligned
        # the scores are displayed in white
        # the background is black
        screen = pygame.display.get_surface()
        # set the background color
        screen.fill((0, 0, 0))
        # set the font
        font = pygame.font.SysFont("Arial", 30)
        for i in range(10):
            # prevent array out of bounds
            if i >= len(self.scores):
                break
            text = font.render(self.scores[i][1], True, white)
            screen.blit(text, (50, 50 + i * 50))
            text = font.render(str(self.scores[i][2]), True, white)
            screen.blit(text, (1000 - text.get_width(), 50 + i * 50))
        pygame.display.update()
        # draw the current user's rank in the bottom right corner, right aligned
        if self.currentUserRank != 0:
            text = font.render("Your rank: " + str(self.currentUserRank), True, white)
            screen.blit(text, (1000 - text.get_width(), 600 - text.get_height()))
            pygame.display.update()
    
# main for testing
if __name__ == "__main__":
    # initialize pygame
    pygame.init()
    # set the screen size
    screen = pygame.display.set_mode(size)
    # set the title
    pygame.display.set_caption("Scoreboard")
    # create the scoreboard
    scoreboard = Scoreboard()
    # load the scores
    scoreboard.load()
    # add a score
    scoreboard.add(100)
    # draw the scoreboard
    scoreboard.draw()
    # wait for the user to close the window
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()