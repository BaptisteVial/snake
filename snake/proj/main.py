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
blue = (0, 0, 255)

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
    checkerboard=Checkerboard(rows = args.lines, colons = args.colons, color1 = black, color2 = white, tile_size = args.square_size) # drawing a black/white checkerboard...
    snake = Snake(snake_color = green, snake_position = SNAKE_POS_INIT, snake_head_color = blue, tile_size = args.square_size)

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
        checkerboard.draw(screen)
        snake.draw(screen)
#        drawing_snake(screen, SNAKE_POS_INIT, args.square_size) #...with the snake on it
        pygame.display.update()
    
    pygame.quit()



### Make a class to represent a square of the checkerboard.

class Tile :
    
    def __init__(self, color, size, row, colon):
        self.color = color
        self.size = size
        self.row = row
        self.colon = colon

    def __repr__(self):
        return f"A {self.color} tile, its size is {self.size}, located {self.position}"

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.colon * self.size, self.row * self.size, self.size, self.size))

### Make a class for the checkerboard.

class Checkerboard :

    def __init__(self, rows, colons, color1, color2, tile_size):
        self.rows = rows
        self.colons = colons
        self.color1 = color1
        self.color2 = color2
        self.tile_size = tile_size
    
    def __repr__(self):
        return f"A {self.color1} and {self.color2} checkerboard, with {self.rows} rows and {self.colons} colons"
    
    def draw(self, screen):    
        for row in range(self.rows):
            for colon in range(self.colons):
                if (row+colon) % 2 == 0:      # alternance test
                    color = self.color1
                else :
                    color = self.color2
                tile = Tile(color, self.tile_size, row, colon)
                tile.draw(screen)
 # we would like to call the Tile class here instead of : pygame.draw.rect(screen, color, (col * square_size, row * square_size, square_size, square_size))

### Make a class for the snake.

class Snake :
    def __init__(self, snake_color, snake_head_color, snake_position, tile_size):
        self.snake_position = snake_position
        self.snake_color = snake_color
        self.snake_tile_size = tile_size
        self.snake_head_color = snake_head_color
    
    def __repr__(self):
        return f"A {self.snake_color} snake, occupying the tiles {self.snake_position} "

    def draw(self, screen):
        for pos in self.snake_position:
            tile = Tile(color=self.snake_color, size = self.snake_tile_size, row = pos[0], colon = pos[1])
            tile.draw(screen)
        tile = Tile(color=self.snake_head_color, size = self.snake_tile_size, row = self.snake_position[0][0], colon = self.snake_position[0][1])
        tile.draw(screen)    
# eventually choose a different color for the head
        
        
