import numpy as np
import random
GO_COLOR = int
EMPTY = GO_COLOR(0)
BLACK = GO_COLOR(1)
WHITE = GO_COLOR(2)
BORDER = GO_COLOR(3)

def is_black_white(color: GO_COLOR) -> bool:
    return color == BLACK or color == WHITE

def is_black_white_empty(color: GO_COLOR) -> bool:
    return color == BLACK or color == WHITE or color == EMPTY

def opponent(color: GO_COLOR) -> GO_COLOR:
    return WHITE + BLACK - color

GO_POINT = np.int32
NO_POINT: GO_POINT = GO_POINT(-1)
MAXSIZE: int = 25
DEFAULT_SIZE: int = 7

def board_array_size(size: int) -> int:
    return size * size + 3 * (size + 1)

def where1d(condition: np.ndarray) -> np.ndarray:
    return np.where(condition)[0]

def coord_to_point(row: int, col: int, board_size: int) -> GO_POINT:
    # TODO might be able to optimize this by using a lookup table
    NS = board_size + 1
    return GO_POINT(NS * row + col)

