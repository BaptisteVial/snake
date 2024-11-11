###  importing useful modules

import argparse
import pygame

### defining default constants

WIDTH_DEF = 400
HEIGHT_DEF = 300
COL_DEF = 20
LIN_DEF = 20
SQUARE_SIZE_DEF = 20
SNAKE_POS_INIT = [(10, 5), (10, 6), (10, 7)]

### for a better readability : defining the useful colors

black = (0,0,0)
white = (255,255,255)
green = (0, 255, 0)

### defining the parser, including : number of colons, of lines, size of the tiles ; allowing to change default parameters


def parse_args():

    parser = argparse.ArgumentParser(description='Some description.')
    # parser.add_argument('-W', '--width', type=int, default=WIDTH_DEF, help="Width of the screen")
    # parser.add_argument('-H', '--height', type=int, default=HEIGHT_DEF, help="Height of the screen")
    parser.add_argument('-C', '--colons', type=int, default=COL_DEF, help="Number of colons")
    parser.add_argument('-L', '--lines', type=int, default=LIN_DEF, help="Number of lines")
    parser.add_argument('-S', '--square_size', type=int, default=SQUARE_SIZE_DEF, help="Size of the tiles")
    args = parser.parse_args()
    
    return args


### drawing a checkerboard on a given screen


def checkerboard(screen, square_size, nb_cols, nb_lines):
    
    for row in range(nb_lines):
        for col in range(nb_cols):
            if (row+col) % 2 == 0:      # alternance test
                color = white
            else :
                color = black
            pygame.draw.rect(screen, color, (col * square_size, row * square_size, square_size, square_size))


### drawing the snake on a given checkerboard, where its position is given by a list of tiles (row,col)


def drawing_snake(screen, snake_positions, square_size):
    color = green
    for pos in snake_positions:
        row, col = pos
        pygame.draw.rect(screen, color, (col * square_size, row * square_size, square_size, square_size))


### defining the playable pygame program


def snake():
    ### initializing the arguments, the screen, the clock...
    args=parse_args()
    pygame.init()
    screen = pygame.display.set_mode( (args.square_size*args.colons, args.square_size*args.lines) )
    clock = pygame.time.Clock()
    running = True  # ending condition : running = False

    while running:
        clock.tick(100) # >> 1 , to have a better speed execution
    # Processing new events (keyboard, mouse)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False  

        screen.fill(white) # filling the screen with white
        checkerboard(screen, args.square_size, args.colons, args.lines) # drawing a black/white checkerboard...
        drawing_snake(screen, SNAKE_POS_INIT, args.square_size) #...with the snake on it
        pygame.display.update()
    
    pygame.quit()
