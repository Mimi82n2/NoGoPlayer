import numpy as np
import random
from board_base import EMPTY, BLACK, WHITE, BORDER, GO_COLOR #BORDER, GO_COLOR required
from typing import List

def is_black_white(color):
    return color == BLACK or color == WHITE

def is_black_white_empty(color):
    return color == BLACK or color == WHITE or color == EMPTY

GO_POINT = np.int32

PASS = None

NULLPOINT = 0

MAXSIZE = 25

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
        # Check board.is_legal on all moves
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
