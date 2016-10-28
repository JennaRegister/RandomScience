import pygame
import numpy as np
from scipy import stats
# Define some colors
BACKGROUND = (107,142,35)
BOXCOLOR = (189,183,107)
NUM_START=15
VIOLET = (138,43,226)
TOMATO = (255,99,71)
SEAGREEN = (50,205,50)
PINK = (219,112,147)
YELLOW=(255,255,0)
CYAN = (0,255,255)
colors = [SEAGREEN,CYAN,VIOLET,PINK,YELLOW,TOMATO]
NUMBOXES=40
# This sets the WIDTH and HEIGHT of each world location
WIDTH = 15
HEIGHT = 15

# This sets the margin between each cell
MARGIN = WIDTH//5

world = [[[] for column in range(NUMBOXES)] for row in range(NUMBOXES)]
# Initialize pygame
pygame.init()
# Set the HEIGHT and WIDTH of the screen
# SCALABLE
WINDOW_SIZE = [(WIDTH+MARGIN)*NUMBOXES+MARGIN,(HEIGHT+MARGIN)*NUMBOXES+MARGIN]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("Utopia")

# Used to manage how fast the screen updates
# How we're gonna do movement --maybe-- and shit
clock = pygame.time.Clock()

# ---------- Set up some objects --------
class Creature:
    def __init__(self, parents=[]):
        if parents == []:
            self.level = np.random.randint(0, 6)
            self.max_energy = 1
            self.x = np.random.randint(0, NUMBOXES)
            self.y = np.random.randint(0, NUMBOXES)
            self.pos = [self.x, self.y]
        else:
            self.level = parents[0].level
            self.max_energy = 1
            self.parents = parents
            self.x = parents[0].x+1 % NUMBOXES
            self.y = parents[0].y+1 % NUMBOXES
            self.pos = [self.x, self.y]
            print("A child is born! All hail the baby Jesus!")


        self.children = []
        self.speed = 1
        self.color = colors[self.level]
        self.prev_move = []

    def move(self):
        bias = .3
        movement = [[0,0]]
        if not (self.x == 0):
            movement.append([-1, 0])
        if not (self.y == 0):
            movement.append([0, -1])
        if not (self.x == NUMBOXES - 1):
            movement.append([1, 0])
        if not (self.y == NUMBOXES-1):
            movement.append([0, 1])

        move = regularize(self, movement, bias)

        self.prev_move = movement[move]

        self.x = self.x + movement[move][0]
        self.y = self.y + movement[move][1]
        self.pos = [self.x, self.y]
        # print(self.to_string())

    def consume(self, food_creature):


        #dictionary manager (collide) will remove the food_creature
        return food_creature

    # creates a new creature with 2 parents and assigns things
    def spawn(self, potential_mate):
        baby = Creature([self, potential_mate])
        self.children.append(baby)
        potential_mate.children.append(baby)
        return baby


    def to_string(self):
        return  'level: ' + str(self.level) + ' color: ' + str(self.color) + ' position: ' + str(self.pos)

# Lenny's crap --> basically, makes it more likely to keep moving in the direction you were already going
def regularize(self, options, bias):
    xk = np.arange(len(options))
    pk = []
    regularized = 1/len(options)
    if self.prev_move in options:
        sum_to_bias = (bias / (len(xk)-1))
        for i in xk:
            if self.prev_move == options[i]:
                pk.append(regularized + bias)
            else:
                pk.append(regularized - sum_to_bias)
    else:
        for i in xk:
            pk.append(1/len(options))

    return np.random.choice(xk, p=pk)

#the "dictionary manager" --> the actual events happen within Creature class
def collide(cA, cB, creatures):
    if cA.level == cB.level:
        if not (cA in cB.children or cB in cA.children):
            baby = cA.spawn(cB)
            add_creature(creatures, baby)
            for i in range(10):
                cA.move()
                cB.move()

    else:
        if cA.level > cB.level:
            remove_creature(creatures, cA.consume(cB))
        else:
            remove_creature(creatures, cB.consume(cA))

# removes a creature from all of the creatures dictionary lists
# Result[1] is a creature
def remove_creature(creatures, food):
    index = creatures['creature'].index(food)
    creatures['pos'].pop(index)
    creatures['level'].pop(index)
    creatures['creature'].pop(index)

#adds a creature to the dictionary
def add_creature(creatures, baby):
    creatures['creature'].append(baby)
    creatures['pos'].append(baby.pos)
    creatures['level'].append(baby.level)

def placeall(creatures):
    #world = [[[] for column in range(NUMBOXES)] for row in range(NUMBOXES)]
    for creature in creatures['creature']:
        # get the position of the current creature
        x, y = creature.x, creature.y
        # get the index of that creature
        selfindex = creatures['creature'].index(creature)
        # if there is another creature (of the creatures we've updated so far) with the same position
        if [x,y] in creatures['pos'][:selfindex]:
            #grab that creature
            other_creature = creatures['creature'][creatures['pos'][:selfindex].index([x,y])]
            creatures['pos'][selfindex] = [x, y]
            #call collide on these buddies
            collide(creature, other_creature, creatures)
        else:
            #if they don't collide, update the positions after movement
            creatures['pos'][selfindex] = [x, y]

        #draw dat shit
        pygame.draw.rect(screen,creature.color,[(MARGIN + WIDTH) * x + MARGIN,(MARGIN + HEIGHT) * y + MARGIN,WIDTH,HEIGHT])

# -------- Main Program Loop -----------

def main():

    cmaker = [Creature() for i in range(NUM_START)]
    creatures = {'creature': cmaker, 'pos': [], 'level': []}
    for creature in cmaker:
        creatures['pos'].append(creature.pos)
        creatures['level'].append(creature.level)

    done = False
    while not done:

        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop


        for creature in creatures['creature']:
            creature.move()
                # Set the screen background
        screen.fill(BACKGROUND)

                # Draw the world
        for row in range(NUMBOXES):
            for column in range(NUMBOXES):
                color = BOXCOLOR
                pygame.draw.rect(screen,color,[(MARGIN + WIDTH) * column + MARGIN,(MARGIN + HEIGHT) * row + MARGIN,WIDTH,HEIGHT])
                placeall(creatures)

                # Limit to 60 frames per second
        clock.tick(30)

                # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # on exit.
    pygame.quit()

main()
