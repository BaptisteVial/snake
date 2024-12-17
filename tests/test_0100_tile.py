import snake

red = (255, 0, 0)


def test_creation():
    t=snake.Tile(row = 1, column = 1, color = red)
    assert t._color == red 