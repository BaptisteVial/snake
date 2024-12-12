### Importing useful modules

import pygame
import argparse
import random
import abc
import enum
from typing import List, Tuple, Iterator

### Class that handles directions

class Dir(enum.Enum):
    """Represents the direction of the snake's movement."""

    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


### Default constants

DEFAULT_WIDTH = 30
DEFAULT_HEIGHT = 30
DEFAULT_TILE_SIZE = 20
DEFAULT_STARTING_SNAKE = [(10, 7), (10, 6), (10, 5)]
DEFAULT_DIRECTION = Dir.RIGHT


### Class that handles the drawing of the game objects

class Board:
    """
    Represents the game board where all objects are drawn.

    Attributes:
        screen (pygame.Surface): The screen to draw objects on.
        tile_size (int): Size of each tile on the board.

    """

    def __init__(self, screen: pygame.Surface, tile_size: int):
        self._screen = screen
        self._tile_size = tile_size
        self._objects: List[GameObject] = []

    def draw(self) -> None:
        """Draws all game objects on the screen."""
        for obj in self._objects:
            for tile in obj.tiles:
                tile.draw(self._screen, self._tile_size)

    def add_object(self, game_object: 'GameObject') -> None:
        """Adds a game object to the board.

        Args:
            gameobject (GameObject): The game object to add.

        """
        self._objects.append(game_object)

class GameObject(abc.ABC):
    """Abstract base class for game objects that are represented by tiles."""

    def __init__(self):
        super().__init__()

    @property
    @abc.abstractmethod
    def tiles(self) -> Iterator['Tile']:  # noqa: D102
        raise NotImplementedError

### Class that handles the drawing of single tiles

class Tile:
    """
    Represents a single tile on the board.

    Attributes:
        row (int): Row position of the tile.
        column (int): Column position of the tile.
        color (Tuple[int, int, int]): Color of the tile (RGB).

    """

    def __init__(self, row, column, color):
        self._row = row
        self._column = column
        self._color = color

    def draw(self, screen, tile_size):
        rect = pygame.Rect(self._column * tile_size, self._row * tile_size, tile_size, tile_size)
        pygame.draw.rect(screen, self._color, rect)

    def __add__(self, other):
        if not isinstance(other, Dir):
            raise ValueError('Type is wrong')
        return Tile(self._row + other.value[1], self._column + other.value[0], self._color)
    
### Class that handles the checkerboard

class CheckerBoard(GameObject):
    """
    Represents the checkerboard pattern on the game board.

    Attributes:
        size (argparse.Namespace): Size of the board.
        color1 (Tuple[int, int, int]): Color for alternating tiles.
        color2 (Tuple[int, int, int]): Alternate color for the tiles.

    """

    def __init__(self, size, color1, color2):
        self._size = size
        self._color1 = color1
        self._color2 = color2

    @property
    def tiles(self):
        for row in range(self._size.height):
            for column in range(self._size.width):
                yield Tile(row=row, column=column, color=self._color1 if (row + column) % 2 == 0 else self._color2)

### Class that handles the snake

class Snake(GameObject):
    """
    Represents the snake in the game.

    Attributes:
        positions (List[Tuple[int, int]]): Initial positions of the snake's segments.
        color (Tuple[int, int, int]): Color of the snake.
        direction (Dir): Direction the snake is moving.

    """

    def __init__(self, positions : list, color : tuple, direction : tuple):
        self._tiles = [Tile(p[0], p[1], color) for p in positions]
        self._color = color
        self._direction = direction

    @property
    def dir(self):
        return self._direction

    @dir.setter
    def dir(self, new_direction):
        self._direction = new_direction

    def __len__(self):
        return len(self._tiles)

    def move(self, grow=False ):
        self._tiles.insert(0, self._tiles[0] + self._direction)
        if not grow:
            self._tiles.pop()

    @property
    def tiles(self):
        return iter(self._tiles)

### Class that handles the fruits

class Fruit(GameObject):
    """
    Represents a fruit on the board.

    Attributes:
        position (Tuple[int, int]): Position of the fruit.
        color (Tuple[int, int, int]): Color of the fruit.

    """

    def __init__(self, position, color):
        self._tiles = [Tile(row=position[0], column=position[1], color=color)]
        self._position = position
        self._color = color

    def eating(self, snake_head):
        return self._position == (snake_head._row, snake_head._column)

    def move(self, size):
        self._position = (random.randint(0, size.height - 1), random.randint(0, size.width - 1))
        self._tiles = [Tile(row=self._position[0], column=self._position[1], color=self._color)]

    @property
    def tiles(self):
        return iter(self._tiles)

def windowsize():
    parser = argparse.ArgumentParser(description='Window size with numbers of tiles.')
    parser.add_argument('-w', '--width', type=int, default=DEFAULT_WIDTH, help="Width in tiles.")
    parser.add_argument('-e', '--height', type=int, default=DEFAULT_HEIGHT, help="Height in tiles.")
    args = parser.parse_args()

    return args

### The gaming loop

def snake():

    size = windowsize()
    pygame.init()
    screen = pygame.display.set_mode((size.width * DEFAULT_TILE_SIZE, size.height * DEFAULT_TILE_SIZE))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Snake - Score: 0")

    board = Board(screen=screen, tile_size=DEFAULT_TILE_SIZE)

    checkerboard = CheckerBoard(size, (0, 0, 0), (255, 255, 255))
    snake = Snake(DEFAULT_STARTING_SNAKE, (0, 255, 0), DEFAULT_DIRECTION)
    fruit = Fruit((3, 3), (255, 0, 0))

    board.add_object(checkerboard)
    board.add_object(snake)
    board.add_object(fruit)

    game_running = True

    while game_running:
        clock.tick(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    game_running = False
                elif event.key == pygame.K_UP and snake.dir != Dir.DOWN:
                    snake.dir = Dir.UP
                elif event.key == pygame.K_DOWN and snake.dir != Dir.UP:
                    snake.dir = Dir.DOWN
                elif event.key == pygame.K_RIGHT and snake.dir != Dir.LEFT:
                    snake.dir = Dir.RIGHT
                elif event.key == pygame.K_LEFT and snake.dir != Dir.RIGHT:
                    snake.dir = Dir.LEFT

        grow = False
        if fruit.eating(snake._tiles[0]):
            grow = True
            fruit.move(size)

        snake.move(grow=grow)

        head = snake._tiles[0]
        if (head._row < 0 or head._row >= size.height or
                head._column < 0 or head._column >= size.width or
                any(t._row == head._row and t._column == head._column for t in list(snake._tiles)[1:])):
            print("Game Over!")
            game_running = False

        board.draw()
        pygame.display.set_caption(f"Snake - Score: {len(snake) - 3}")
        pygame.display.update()

    pygame.quit()
    quit(0)
