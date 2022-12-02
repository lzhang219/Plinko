# This creates a roulette style "layout" betting board, with colours red and black and numbers 1-8 and 0 to the side
#
# Path: betting.py
#
# Import submodules
from constants import *
from objects import *
import sys
class Layout:
    def __init__(self):
        self.score = 3
        self.colourbets = []
        self.numberbets = []
        for index, colour in enumerate(colours.items()):
            self.colourbets.append(ColourBet(colour[1][1], colour[1][0], colour[0], 50, 400/len(colours)*index+100, 300, 400/len(colours)))
        # numbers 1,2,3,4 will be on the top row
        # numbers 5,6,7,8 will be on the bottom row
        # number 0 will occupy a cell to the very right of the board spanning both rows
        for number, (colour, odds) in numbers.items():
            if number == 0:
                self.numberbets.append(NumberBet(odds, number, colour,  900, 100, 100, 400))
            elif number < 5:
                self.numberbets.append(NumberBet(odds, number, colour, 300+(number-1)*150, 100, 150, 200))
            else:
                self.numberbets.append(NumberBet(odds, number, colour, 300+(number-5)*150, 300, 150, 200))
    def draw(self):
        # green background
        screen.fill((0, 127, 0))
        for bet in self.colourbets:
            bet.draw()
        for bet in self.numberbets:
            bet.draw()
        # draw the score in the top right corner using right aligned text
        font = pygame.font.SysFont("Arial", 30)
        scoretext = font.render("Points: " + str(self.score), True, (255, 255, 255))
        screen.blit(scoretext, (1050 - scoretext.get_width(), 0))
        # draw text to the bottom right corner to tell the user to press enter to start the game
        instructions = font.render("Press ENTER when you are done placing bets.", True, (255, 255, 255))
        screen.blit(instructions, (1050 - instructions.get_width(), 600 - instructions.get_height()))
    def placebet(self, x, y):
        # check if the user clicked on a colour bet
        for bet in self.colourbets:
            if bet.x <= x <= bet.x + bet.width and bet.y <= y <= bet.y + bet.height:
                bet.place(self)
                return
        # check if the user clicked on a number bet
        for bet in self.numberbets:
            if bet.x <= x <= bet.x + bet.width and bet.y <= y <= bet.y + bet.height:
                bet.place(self)
                return
        return
    def result(self, colour, number):
        # check if the user won any colour bets
        for bet in self.colourbets:
            if bet.colour == colour:
                self.score += bet.win()
            else:
                bet.lose()
        # check if the user won any number bets
        for bet in self.numberbets:
            if bet.number == number:
                self.score += bet.win()
            else:
                bet.lose()


class ColourBet:
    def __init__(self, odds, colour, colourname, x, y, width, height):
        self.odds = odds
        self.colour = colour
        self.colourname = colourname
        self.bet = 0
        self.winnings = 0
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def bet(self, amount):
        self.bet = amount
    def win(self):
        self.winnings = self.bet * self.odds
        self.bet = 0
        return self.winnings
    def lose(self):
        self.bet = 0
    def draw(self):
        # draw a rectangle
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))
        # border around the rectangle to make it stand out
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.height), 1)
        # add text with the name of the colour bet on
        font = pygame.font.SysFont("Arial", 20)
        text = font.render(self.colourname, True, (0, 0, 0) if self.colour[0]+self.colour[1]+self.colour[2] > 384 else (255, 255, 255))
        # add text to the rectangle in a colour that contrasts with the colour of the rectangle
        text1 = font.render("Odds: "+str(self.odds)+"x", True, (0, 0, 0) if self.colour[0]+self.colour[1]+self.colour[2] > 384 else (255, 255, 255))
        # add text with the amount of money bet on this slot
        text2 = font.render("Bet: "+str(self.bet), True, (0, 0, 0) if self.colour[0]+self.colour[1]+self.colour[2] > 384 else (255, 255, 255))
        # render the text
        screen.blit(text, (self.x+5, self.y+5))
        screen.blit(text1, (self.x+5, self.y+25))
        screen.blit(text2, (self.x+5, self.y+45))
    def place(self, layout):
        # if the user clicks on a bet, they can bet money on it
        # user input amount of money to bet
        # new main loop to get user input
        bet = 0
        while True:
            continueloop = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    if event.key == pygame.K_RETURN:
                        # user has finished entering bet amount
                        continueloop = False
                    if event.key == pygame.K_BACKSPACE:
                        # remove the last digit from the bet
                        bet = bet // 10
                    if event.key >= pygame.K_0 and event.key <= pygame.K_9:
                        # add the number the user just pressed to the bet
                        bet = bet * 10 + event.key - pygame.K_0
            # draw the screen
            # draw the screen
            screen.fill((255, 255, 255))
            # put the instructions on the screen in large text
            inputfont = pygame.font.SysFont("Arial", 50)
            text = inputfont.render("Enter the amount you want to bet on "+self.colourname, True, (0, 0, 0))
            text1 = inputfont.render("Press ENTER to confirm your bet of "+str(bet), True, (0, 0, 0))
            text2 = inputfont.render("Press ESCAPE to cancel your bet", True, (0, 0, 0))
            # render the text centered on the screen in the x axis and 1/4 of the way down the screen in the y axis
            centerx = (screen.get_width() - text.get_width()) // 2
            centery = (screen.get_height() - text.get_height()) // 4
            screen.blit(text, (centerx, centery))
            centerx = (screen.get_width() - text1.get_width()) // 2
            screen.blit(text1, (centerx, centery+100))
            centerx = (screen.get_width() - text2.get_width()) // 2
            screen.blit(text2, (centerx, centery+200))
            pygame.display.update()
            if not continueloop:
                break
        # check if user can afford the bet
        # if they can, subtract the bet from their score
        # if they can't, tell them they can't afford the bet
        # if they can, add the bet to the bet variable
        if layout.score >= bet:
            layout.score -= bet
            self.bet = bet
            return
        else:
            # draw the screen
            screen.fill((255,255,255))
            # use big red text to tell the user they can't afford the bet
            font = pygame.font.SysFont("Arial", 50)
            text = font.render("You can't afford to bet that much!", True, (255, 0, 0))
            # render the text centered on the screen in the x axis and 1/4 of the way down the screen in the y axis
            centerx = (screen.get_width() - text.get_width()) // 2
            centery = (screen.get_height() - text.get_height()) // 4
            screen.blit(text, (centerx, centery))
            pygame.display.update()
            # wait for the user to press enter
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            return
        
        
        






class NumberBet:
    def __init__(self, odds, number, colour, x, y, width, height):
        self.odds = odds
        self.number = number
        self.bet = 0
        self.winnings = 0
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def bet(self, amount):
        self.bet = amount
    def win(self):
        self.winnings = self.bet * self.odds
        self.bet = 0
        return self.winnings
    def lose(self):
        self.bet = 0
    def draw(self):
        # draw a rectangle
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))
        # add text with the number bet on
        font = pygame.font.SysFont("Arial", 20)
        text = font.render(str(self.number), True, (0, 0, 0) if self.colour[0]+self.colour[1]+self.colour[2] > 384 else (255, 255, 255))
        # add text to the rectangle in a colour that contrasts with the colour of the rectangle
        text1 = font.render("Odds: "+str(self.odds)+"x", True, (0, 0, 0) if self.colour[0]+self.colour[1]+self.colour[2] > 384 else (255, 255, 255))
        # add text with the amount of money bet on this slot
        text2 = font.render("Bet: "+str(self.bet), True, (0, 0, 0) if self.colour[0]+self.colour[1]+self.colour[2] > 384 else (255, 255, 255))
        # render the text
        screen.blit(text, (self.x+5, self.y+5))
        screen.blit(text1, (self.x+5, self.y+25))
        screen.blit(text2, (self.x+5, self.y+45))
    def place(self, layout):
        # if the user clicks on a bet, they can bet money on it
        # user input amount of money to bet
        # new main loop to get user input
        # copypasted code with some modifications :P
        bet = 0
        while True:
            continueloop = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    if event.key == pygame.K_RETURN:
                        # user has finished entering bet amount
                        continueloop = False
                    if event.key == pygame.K_BACKSPACE:
                        # remove the last digit from the bet
                        bet = bet // 10
                    if event.key >= pygame.K_0 and event.key <= pygame.K_9:
                        # add the number the user just pressed to the bet
                        bet = bet * 10 + event.key - pygame.K_0
            # draw the screen
            screen.fill((255, 255, 255))
            # put the instructions on the screen in large text
            inputfont = pygame.font.SysFont("Arial", 50)
            text = inputfont.render("Enter the amount you want to bet on "+str(self.number), True, (0, 0, 0))
            text1 = inputfont.render("Press ENTER to confirm your bet of "+str(bet), True, (0, 0, 0))
            text2 = inputfont.render("Press ESCAPE to cancel your bet", True, (0, 0, 0))
            # render the text centered on the screen in the x axis and 1/4 of the way down the screen in the y axis
            centerx = (screen.get_width() - text.get_width()) // 2
            centery = (screen.get_height() - text.get_height()) // 4
            screen.blit(text, (centerx, centery))
            centerx = (screen.get_width() - text1.get_width()) // 2
            screen.blit(text1, (centerx, centery+100))
            centerx = (screen.get_width() - text2.get_width()) // 2
            screen.blit(text2, (centerx, centery+200))
            pygame.display.update()
            if not continueloop:
                break
        # check if user can afford the bet
        # if they can, subtract the bet from their score
        # if they can't, tell them they can't afford the bet
        # if they can, add the bet to the bet variable
        if layout.score >= bet:
            layout.score -= bet
            self.bet = bet
            return
        else:
            # draw the screen
            screen.fill((255,255,255))
            # use big red text to tell the user they can't afford the bet
            inputfont = pygame.font.SysFont("Arial", 50)
            text = inputfont.render("You can't afford to bet that much!", True, (255, 0, 0))
            # render the text centered on the screen in the x axis and 1/4 of the way down the screen in the y axis
            centerx = (screen.get_width() - text.get_width()) // 2
            centery = (screen.get_height() - text.get_height()) // 4
            screen.blit(text, (centerx, centery))
            pygame.display.flip()
            # wait for the user to press enter
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            return

# TBH I could totally do this with an abstract/parent class and then just have a colour slot and a number slot class that inherit from it
# but I'm not going to do that because I'm lazy also I'm not sure how to do that in python

# test code if this is run as a standalone file
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1100, 600))
    font = pygame.font.SysFont("Arial", 20)
    layout = Layout()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                layout.placebet(*(pygame.mouse.get_pos()))
        screen.fill(black)
        layout.draw()
        pygame.display.update()