### Importing useful modules

import pygame
import argparse
import random as rd
import abc
import enum
from typing import List, Tuple,Iterator

### Class that handles directions

class Dir(enum.Enum):
    """Represents the direction of the snake's movement."""

    DOWN=(1,0)
    UP=(-1,0)
    LEFT=(0,-1)
    RIGHT=(0,1)

### Class that handles observers

class Observer(abc.ABC): 

    def __init__(self) -> None:
        """Define the observer."""
        super().__init__()

    def notify_object_eaten(self, obj: "GameObject") -> None :
        """Notify if an object is eaten."""


    def notify_object_moved(self, obj: "GameObject") -> None:
        """Notify an object is moved."""


    def notify_collision(self, obj : "GameObject") -> None:
        """Notify a collision."""

### Class that handles subjects

class Subject(abc.ABC):  # noqa: B024, D101

    def __init__(self) -> None:
        """Define the subject."""
        super().__init__()
        self._observers : list[Observer] = []

    @property
    def observers(self) -> list[Observer]:
        """Return the the observers."""
        return self._observers

    def attach_obs(self, obs: Observer) -> None:
        """Attach the observers."""
        print(f"Attach {obs} as observer of {self}.")  # noqa: T201
        self._observers.append(obs)

    def detach_obs(self, obs: Observer) -> None:
        """Detach the observers."""
        print(f"Detach observer {obs} from {self}.")  # noqa: T201
        self._observers.remove(obs)


### Default constants

DEFAULT_LINES=20 #Nombre de lignes par defaut
DEFAULT_COLUMNS=30 #Nombre de colonnes par defaut
DEFAULT_SIZE= 50# Taille du carre par defaut

### Class that handles the drawing of the game objects

class Board(Subject, Observer) :
    """Define the board used to draw globally."""

    def __init__(self, screen : pygame.Surface, tile_size : int, nb_rows : int, nb_cols : int)-> None :
        self._screen=screen
        self._tile_size=tile_size
        self._object : list[object]=[]
        self._nb_rows=nb_rows
        self._nb_cols=nb_cols

    def draw(self) -> None:
        """Draw the tiles for the objects."""
        for obj in self._object :
            for tile in obj.tiles:
                tile.draw(self._screen,self._tile_size)


    def add_object(self, gameobject: "GameObject") -> None:
        """Add the objects as observers."""
        self._object.append(gameobject)
        gameobject.attach_obs(self)

    def remove_object(self, gameobject : "GameObject") -> None:
        """Remove the objects of the observers."""
        gameobject.detach_obs(self)
        self._object.remove(gameobject)

    def create_fruit(self) -> "Fruit" :
        """Create fruits."""
        fruit=None
        while fruit is None or self.detect_collision(fruit) is not None :
            fruit=Fruit(color_fruit=pygame.Color("red"), col=rd.randint(0,self._nb_cols-1), row=rd.randint(0, self._nb_rows-1))

    def detect_collision(self, obj : "GameObject") :
        """Detect wether or not there has been a collision."""
        for o in self._object :
            if o != obj and not o.background and o in obj :
                return o
        return None


    def notify_object_moved(self, obj:"GameObject") -> None :
        """Detecte the collision with others."""  # noqa: D401
        o=self.detect_collision(obj)
        if o is not None:
            obj.notify_collision(o)

    def notify_object_eaten(self, obj:"GameObject")  -> None :
        """Remove the old fruit and create a new one."""
        self.remove_object(obj)
        self.create_fruit()


class GameObject(Subject, Observer) :
    """Defining a class that handles game objects."""

    def __init__(self) -> None :
        """Define the GameObject."""
        super().__init__()

    def __contains__(self, obj:object)-> bool :
        """Define the in for an object."""
        if isinstance(obj, GameObject) :
            return any(t in obj.tiles for t in self.tiles)
        return False

    @property
    @abc.abstractmethod
    def tiles(self) -> None :
        """Create the tiles'property."""
        raise NotImplementedError # every object that inherits from GameObject
                                  #  must have a tiles property

    @property
    def background(self) -> bool :
        """Create the background's property."""
        return False # by default, gameobject is not a background

### Class that handles the drawing of single tiles

class Tile:
    """
    Represents a single tile on the board.

    Attributes:
        row (int): Row position of the tile.
        column (int): Column position of the tile.
        color (Tuple[int, int, int]): Color of the tile (RGB).

    """

    def __init__(self,row : int ,column : int , color : tuple) -> None:
        """Initialize the tile."""
        self._color=color
        self._row=row
        self._column=column

    def __repr__(self) -> str:
        """Represent a tile."""
        return f"({self._row}, {self._column})"

    @property
    def coord(self) -> tuple :
        """Return the coordinates of a tile."""
        return (self._row, self._column)

    def draw(self, screen : pygame.Surface, tile_size : int) -> None:
        """Draw the tiles."""
        rect = pygame.Rect(self._column*tile_size, self._row*tile_size, tile_size, tile_size)
        pygame.draw.rect(screen, self._color, rect)

### Class that handles the checkerboard

class CheckerBoard(GameObject):
    """
    Represents the checkerboard pattern on the game board.

    Attributes:
        size (argparse.Namespace): Size of the board.
        color1 (Tuple[int, int, int]): Color for alternating tiles.
        color2 (Tuple[int, int, int]): Alternate color for the tiles.

    """

    def __init__(self, color_1 : tuple, color_2 : tuple , nb_rows : int , nb_columns : int) -> None :
        """Initialize the Checkerboard."""
        self._color_1=color_1
        self._color_2=color_2
        self._nb_rows=nb_rows
        self._nb_columns=nb_columns

    @property
    def background(self)->bool:
        """Says the checkerboard is a background."""
        return True

    @property
    def tiles(self)-> None :
        """Generate the tiles."""
        for column in range(self._nb_columns) :
            for row in range(self._nb_rows) :
                yield(Tile(row=row, column=column, color=self._color_1 if (column+row)%2==0 else self._color_2))

### Class that handles the snake

class Snake(GameObject):
    """
    Represents the snake in the game.

    Attributes:
        positions (List[Tuple[int, int]]): Initial positions of the snake's segments.
        color (Tuple[int, int, int]): Color of the snake.
        direction (Dir): Direction the snake is moving.

    """

    def __init__(self, tiles : list[Tile], direction : Dir) -> None :
        """Define the parameters of the snake."""
        self._tiles=tiles
        self._direction=direction
        self._size=len(self._tiles)

    @classmethod
    def create_from_pos(cls, color : tuple,row : int , column : int, size : int, direction : Dir) -> "Snake" :  # noqa: E501
        """Create the snake."""
        tiles=[Tile(row, column+p, color) for p in range(size)]
        return Snake(tiles=tiles, direction=direction)

    def __len__(self) -> int :
        """Give the len of the snake, useful for the score."""
        return len(self._tiles)


    @property
    def tiles (self) -> None :
        """Return the list of the tiles."""
        iter(self._tiles)

    @property
    def dir(self) -> Dir:
        """Return the direction."""
        return self._direction

    @dir.setter
    def dir(self, new_direction: Dir)-> None:
        """Return the new direction."""
        self._direction = new_direction

     # making the snake move
    def move(self) -> None:
        """Move the snake one tile."""
        #add a new head
        x,y=self._tiles[0].coord
        coord=(x + self._direction.value[0], y + self._direction.value[1])
        self._tiles.insert(0, Tile(coord[0], coord[1], color=pygame.Color("green")))

        for obs in self.observers :
            obs.notify_object_moved(self)

        if self._size < len(self._tiles) :
            self._tiles=self._tiles[:self._size]

    def notify_collision(self, obj : GameObject)-> None :
        """Notify an eatable object has been eaten."""
        if isinstance(obj, Fruit) :
            self._size+=1
            for obs in self._observers :
                obs.notify_object_eaten(obj)

### Class that handles the fruits

class Fruit(GameObject):
    """
    Represents a fruit on the board.

    Attributes:
        position (Tuple[int, int]): Position of the fruit.
        color (Tuple[int, int, int]): Color of the fruit.

    """

    def __init__(self, color_fruit : tuple , col : int , row : int) -> None :
        """Define the fruit."""
        self._color_fruit=color_fruit
        self._col=col
        self._row=row
        self._tiles=[Tile(self._row, self._col,self._color_fruit)]

    @property
    def tiles(self) -> None:
        """Return the tiles."""
        iter(self._tiles)

    @property
    def coord(self)->tuple :
        """Return the coordonates of the fruit."""
        return (self._row, self._col)

def windowsize():
    """Allows to modify the size of the playing window."""
    parser = argparse.ArgumentParser(description='Window size with numbers of tiles.')
    parser.add_argument('-w', '--width', type=int, default=DEFAULT_WIDTH, help="Width in tiles.")
    parser.add_argument('-e', '--height', type=int, default=DEFAULT_HEIGHT, help="Height in tiles.")
    args = parser.parse_args()

    return args

### The gaming loop

def snake() -> None:
    """Code the entire game."""
    color_1=(0,0,0)
    colors_2=(255,255,255)

    columns=30
    rows=20
    size=30

    height=rows*size
    width=columns*size

    color_sna=(0,255,0)
    #color_head=(0,0,255)  # noqa: ERA001
    r_sna=10 # ligne de départ du snake
    c_sna=5 # colonne de départ (position de la tête)
    size_sna=5

    speed=5

    color_fruit=(255,0,0)
    pos_fruit_1=[3,3] #row, column

    direction = Dir.LEFT #the snake starts by moving towards left

    screen = pygame.display.set_mode( (width, height) )

    MyCheckerBoard=CheckerBoard(color_1,colors_2,rows,columns)

    MySnake=Snake.create_from_pos(color_sna, r_sna, c_sna, size_sna, direction)
    Myfruit=Fruit(color_fruit, pos_fruit_1[1],pos_fruit_1[0])
    score=0


    board=Board(screen=screen, tile_size=size, nb_rows=rows, nb_cols=columns)
    board.add_object(MyCheckerBoard) # the order matters ! checkerboard first
    board.add_object(MySnake)
    board.add_object(Myfruit)

    pygame.init()

    clock = pygame.time.Clock()

    game=True
    while game is True:

        clock.tick(speed)

        for event in pygame.event.get():
            #quit game
            if event.type == pygame.QUIT:
                game=False
            if event.type == pygame.KEYDOWN : #on precise qu'il s'agit d'un evnt qui concerne le clavier
                if event.key ==pygame.K_q :
                    game=False


                if event.key==pygame.K_RIGHT :
                    MySnake.dir=Dir.RIGHT
                    MySnake.move()
                    #score=Myfruit.collusion(MySnake, pos_fruit_1, pos_fruit_2, score)
                    direction=Dir.RIGHT
                    break #prevent from going immediately back


                if event.key == pygame.K_LEFT :
                    MySnake.dir=Dir.LEFT
                    MySnake.move()
                    #score=Myfruit.collusion(MySnake, pos_fruit_1, pos_fruit_2, score)
                    direction=Dir.LEFT
                    break


                if event.key == pygame.K_UP :
                    MySnake.dir=Dir.UP
                    MySnake.move()
                    #score=Myfruit.collusion(MySnake, pos_fruit_1, pos_fruit_2, score)
                    direction=Dir.UP
                    break

                if event.key == pygame.K_DOWN :
                    MySnake.dir=Dir.DOWN
                    MySnake.move()
                    #score=Myfruit.collusion(MySnake, pos_fruit_1, pos_fruit_2, score)
                    direction =Dir.DOWN
                    break

        score=len(MySnake)
        board.draw()

        pygame.display.set_caption(f"Ecran de jeu {score}")



        pygame.display.update()


    pygame.quit()