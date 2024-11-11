import argparse
import pygame
WIDTH_DEF = 400
HEIGHT_DEF = 300
COL_DEF = 20
LIN_DEF = 20
SQUARE_SIZE_DEF = 20


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
    # parser.add_argument('-W', '--width', type=int, default=WIDTH_DEF, help="Width of the screen")
    # parser.add_argument('-H', '--height', type=int, default=HEIGHT_DEF, help="Height of the screen")
    parser.add_argument('-C', '--colons', type=int, default=COL_DEF, help="Number of colons")
    parser.add_argument('-L', '--lines', type=int, default=LIN_DEF, help="Number of lines")
    parser.add_argument('-S', '--square_size', type=int, default=SQUARE_SIZE_DEF, help="Size of checkers' squares")
    args = parser.parse_args()
    return args

def checkerboards(screen, square_size, nb_cols, nb_lines):
    color = (0, 0, 0) # black
    for i in range(1, nb_lines):
        for j in range(1, nb_cols):
            rect = pygame.Rect(, top, square_size, square_size)
            pygame.draw.rect(screen, color, rect)

def snake():
    args=parse_args()
    pygame.init()
    screen = pygame.display.set_mode( (args.square_size*args.colons, args.square_size*args.lines) )
    clock = pygame.time.Clock()
    var_quit = True

    while var_quit:

    # Wait one second, starting from last display or now
        clock.tick(100) # way more than one, to have a better speed execution
    # Process new events (keyboard, mouse)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                var_quit = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    var_quit = False  

        screen.fill( (255, 255, 255) ) # Fill screen with white
        checkerboards(screen, args.square_size, args.colons, args.lines)
        pygame.display.update()
    pygame.quit()
