import csv
import pygame
from constants import *
import os
import json

class Scoreboard:
    def __init__(self):
        self.scores = []
        self.load()
    # I LOVE COPYING CODE!
    def load(self):
        # load the scores from the file saved in the same directory as the program in format:
        # name, score (separated by a comma)
        if os.path.isfile("scores.csv"):            
            with open("scores.csv", "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    # prevent empty lines
                    if len(row) > 0:
                        self.scores.append(row)
        print(json.dumps(self.scores, indent=4))
    def save(self):
        # sort the scores
        self.sort()
        # overwrite the scores file with the new saved scores in the format
        # name, score (separated by a comma)
        # without empty lines
        # don't save more than 20 scores
        with open("scores.csv", "w") as f:
            writer = csv.writer(f)
            for i in range(20):
                # prevent array out of bounds
                if i >= len(self.scores):
                    break
                writer.writerow(self.scores[i])
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
        self.scores.append([name, score])
        self.save()
    def sort(self):
        # sort the scores if there are more than 1
        if len(self.scores) > 1:
            self.scores.sort(key=lambda x: int(x[1]), reverse=True)
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
            text = font.render(self.scores[i][0], True, white)
            screen.blit(text, (50, 50 + i * 50))
            text = font.render(str(self.scores[i][1]), True, white)
            screen.blit(text, (1000 - text.get_width(), 50 + i * 50))
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