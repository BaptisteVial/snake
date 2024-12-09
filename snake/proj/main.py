###  importing useful modules

import argparse
import pygame

### defining default constants

WIDTH_DEF = 400
HEIGHT_DEF = 300
COL_DEF = 20
LIN_DEF = 20
SQUARE_SIZE_DEF = 20
SNAKE_POS_INIT = [(10, 7), (10, 6), (10, 5)]

### for a better readability : defining the useful colors

black = (0,0,0)
white = (255,255,255)
green = (0, 255, 0)
dark_green = (4, 175, 32)
blue = (0, 0, 255)
red = (255,0,0)

###  for a better readability : defining the directions

up = (-1,0)
down = (1,0)
right = (0,1)
left = (0,-1)

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
    
    ### initializing the arguments, the screen, the clock
    args=parse_args()
    pygame.init()
    screen = pygame.display.set_mode( (args.square_size*args.colons, args.square_size*args.lines) )
    clock = pygame.time.Clock()
    running = True  # ending condition : running = False
    
    ### initializing the grid
    checkerboard=Checkerboard(rows = args.lines, colons = args.colons, color1 = black, color2 = white, tile_size = args.square_size)
    snake = Snake(snake_color = green, snake_position = SNAKE_POS_INIT, snake_head_color = dark_green, tile_size = args.square_size)

    ### initializing the fruit(s)
    fruits = [
        Fruit(position=(3, 3), color=red, size=args.square_size),
        Fruit(position=(15, 10), color=red, size=args.square_size)
    ]
    current_fruit_index = 0  # start with the first fruit
    score = 0

    while running:
        clock.tick(10) # > 1 , to have a better speed execution
    # Processing new events (keyboard, mouse)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                if event.key == pygame.K_UP:
                    snake.change_direction(up)
                if event.key == pygame.K_DOWN:
                    snake.change_direction(down)
                if event.key == pygame.K_LEFT:
                    snake.change_direction(left)
                if event.key == pygame.K_RIGHT:
                    snake.change_direction(right)

        ### Move snake

        grow = False
        if fruits[current_fruit_index].position in snake:
            grow = True
            score = score + 1
            current_fruit_index = (current_fruit_index + 1) % len(fruits) # notation that will be adapted to longer lists

        snake.move(grow=grow)

        ### Check collisions
        if snake.check_collision(args.lines, args.colons):
            print("Game Over!")
            running = False

        pygame.display.set_caption(f"Snake Game - Score: {score}") # display the current score
        screen.fill(white)
        checkerboard.draw(screen)
        snake.draw(screen)
        fruits[current_fruit_index].draw(screen)
        pygame.display.update()
    
    pygame.quit()



### Make a class to represent a square of the checkerboard

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

### Make a class for the checkerboard

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
 
### Make a class for the snake

class Snake :
    def __init__(self, snake_color, snake_head_color, snake_position, tile_size):
        self.snake_position = snake_position
        self.snake_color = snake_color
        self.snake_tile_size = tile_size
        self.snake_head_color = snake_head_color
        self.direction = right
    
    def __repr__(self):
        return f"A {self.snake_color} snake, occupying the tiles {self.snake_position} "

    def __contains__(self, position):
        return position in self.snake_position

    def draw(self, screen):
        for pos in self.snake_position:
            tile = Tile(color=self.snake_color, size = self.snake_tile_size, row = pos[0], colon = pos[1])
            tile.draw(screen)
        tile = Tile(color=self.snake_head_color, size = self.snake_tile_size, row = self.snake_position[0][0], colon = self.snake_position[0][1])
        tile.draw(screen) # eventually choose a different color for the head
        
    def move(self, grow=False):
        head = self.snake_position[0]           # Calculate new head position
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])   # Add new head
        if grow:
            self.snake_position = [new_head] + self.snake_position     # Keep the tail
        else:
            self.snake_position = [new_head] + self.snake_position[:-1]      # Remove the tail  

    def change_direction(self, new_direction):
        opposite_direction = (-self.direction[0], -self.direction[1])
        if new_direction != opposite_direction:     # Prevent reversing on itself !!
            self.direction = new_direction   
    
    def check_collision(self, rows, cols):
    # Check if the snake collides with walls or itself
        head = self.snake_position[0]
        ###print(f"Checking collision for head at {head} within grid ({rows}, {cols})")
        if head[0] < 0 or head[1] < 0 or head[0] >= rows or head[1] >= cols:
            ###print("Collision with wall detected!")
            return True
        if head in self.snake_position[1:]:
            ###print("Collision with self detected!")
            return True
        return False
    

### Make a class for the fruits

class Fruit:
    def __init__(self, position, color, size):
        self.position = position
        self.color = color
        self.size = size

    def __repr__(self):
        return f"A {self.color} fruit, occupying the tiles {self.position} "

    def draw(self, screen):
        row, col = self.position
        pygame.draw.rect(screen, self.color, (col * self.size, row * self.size, self.size, self.size))

        
