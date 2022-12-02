"""
board_util.py
Utility functions for Go board.
"""

import numpy as np
import random
from board_base import EMPTY, BLACK, WHITE, BORDER, GO_COLOR
from typing import List

def is_black_white(color):
    return color == BLACK or color == WHITE


def is_black_white_empty(color):
    return color == BLACK or color == WHITE or color == EMPTY


"""
A GO_POINT is a point on a Go board.
It is encoded as a 32-bit integer, using the numpy type.
"""
GO_POINT = np.int32

"""
Encoding of special pass move
"""
PASS = None

"""
Encoding of "not a real point", used as a marker
"""
NULLPOINT = 0

"""
The largest board we allow.
To support larger boards the coordinate printing in
GtpConnection.format_point needs to be changed.
"""
MAXSIZE = 25

"""
where1d: Helper function for using np.where with 1-d arrays.
The result of np.where is a tuple which contains the indices
of elements that fulfill the condition.
For 1-d arrays, this is a singleton tuple.
The [0] indexing is needed to extract the result from the singleton tuple.
"""
def where1d(condition):
    return np.where(condition)[0]


def coord_to_point(row, col, boardsize):
    NS = boardsize + 1
    return NS * row + col


class GoBoardUtil(object):
    @staticmethod
    def generate_legal_moves(board, color):
        moves: np.ndarray[GO_POINT] = board.get_empty_points()
        legal_moves: List[GO_POINT] = []
        
        for move in moves:
            if board.is_legal(move, color):
                legal_moves.append(move)
        return legal_moves

    @staticmethod
    def generate_random_move(board, color):
        # New Random Move Generator
        moves: np.ndarray[GO_POINT] = board.get_empty_points()
        # While moves is not empty
        while moves.size > 0:
            # idx of move to remove
            idx = random.randint(0, moves.size - 1)
            # Remove move from moves
            move = moves[idx]
            moves = np.delete(moves, idx)

            if board.is_legal(move, color):
                return move
        return None

    @staticmethod
    def generate_random_moves(board, use_eye_filter):
        color = board.current_player
        legal_moves = GoBoardUtil.generate_legal_moves(board, color)
        random.shuffle(legal_moves)
        return legal_moves

    @staticmethod
    def opponent(color):
        return WHITE + BLACK - color

    @staticmethod
    def get_twoD_board(goboard):
        size = goboard.size
        board2d = np.zeros((size, size), dtype=GO_POINT)
        for row in range(size):
            start = goboard.row_start(row + 1)
            board2d[row, :] = goboard.board[start : start + size]
        board2d = np.flipud(board2d)
        return board2d
