import argparse
import pygame
WIDTH_DEF = 400
HEIGHT_DEF = 300

def hello():
    parser = argparse.ArgumentParser(description='Some description.')
    parser.add_argument('-a', help="A text explaining what is the use of the -a option and what type of value it takes.")
    args = parser.parse_args()

def hello2():
    print("Hello!")

def add(x, y):
    return x + y

def parse_args():
    parser = argparse.ArgumentParser(description='Some description.')
    parser.add_argument('-W', '--width', type=int, default=WIDTH_DEF, help="Width of the screen")
    parser.add_argument('-H', '--height', type=int, default=HEIGHT_DEF, help="Height of the screen")
    args = parser.parse_args()
    return args

def blankscreen():
    args=parse_args()
    pygame.init()
    screen = pygame.display.set_mode( (args.width, args.height) )
    clock = pygame.time.Clock()

    while True:

    # Wait one second, starting from last display or now
        clock.tick(1)
    # Process new events (keyboard, mouse)
        for event in pygame.event.get():
            pass # do nothing for the moment
        screen.fill( (255, 255, 255) ) # Fill screen with green
        color = (0, 0, 255) # blue
        
        pygame.display.update()
