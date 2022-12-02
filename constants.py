# Define the colors we will use in RGB format
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Set the height and width of the screen
size = (1100, 600)
# TODO: dynamic size

slotsinfo = [("",(0,127,0)),("1", black), ("2", red), ("3", black), ("4", red), ("0", white), ("5", red), ("6", black), ("7", red), ("8", black), ("", (0,127,0))]

# There are 8 layers of pegs
# Each layer contains 3,4,5,6,7,8,9,8 pegs respectively
# define a list of how many pegs are in each layer
pegnos = [3, 4, 5, 6, 7, 8, 9, 8]

# define a list of colours and odds
colours = {"Red":(red, 3), "Black":(black, 6)}
# define a list of numbers and odds
numbers = {1:(black, 45), 2:(red, 15), 3:(black, 8), 4:(red, 6), 5:(red, 6), 6:(black, 8), 7:(red, 15), 8:(black, 45), 0:(white, 6)}
