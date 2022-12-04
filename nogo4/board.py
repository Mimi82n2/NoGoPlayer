import numpy as np
from typing import List, Tuple
from board_base import(
    opponent
)
from board_util import (
    GoBoardUtil,
    BLACK,
    WHITE,
    EMPTY,
    BORDER,
    PASS,
    is_black_white,
    is_black_white_empty,
    coord_to_point,
    where1d,
    MAXSIZE,
    GO_POINT,
    GO_COLOR,
)

class GoBoard(object):
    def __init__(self, size):
        self.reset(size)

    def reset(self, size):
        self.size: int = size
        self.NS: int = size + 1
        self.WE: int = 1
        self.current_player: GO_COLOR = BLACK
        self.maxpoint = size * size + 3 * (size + 1)
        self.board = np.full(self.maxpoint, BORDER, dtype=GO_POINT)
        self._initialize_empty_points(self.board)
        self._initialize_neighbors()

    def _initialize_neighbors(self) -> None:
        self.neighbors: List[List[GO_POINT]] = []
        for point in range(self.maxpoint):
            if self.board[point] == BORDER:
                self.neighbors.append([])
            else:
                self.neighbors.append(self._on_board_neighbors(GO_POINT(point)))  

    def _on_board_neighbors(self, point: GO_POINT) -> List:
        nbs: List[GO_POINT] = []
        for nb in self._neighbors(point):
            if self.board[nb] != BORDER:
                nbs.append(nb)
        return nbs

    def copy(self):
        b = GoBoard(self.size)
        b.current_player = self.current_player
        b.board = np.copy(self.board)
        return b

    def get_color(self, point):
        return self.board[point]

    def pt(self, row, col):
        return coord_to_point(row, col, self.size)

    def is_legal(self, point: GO_POINT, color: GO_COLOR) -> bool:
        self.board[point] = color
        neighbors = self.neighbors[point]
        for nb in neighbors:
            if self.board[nb] == opponent(color):
                if self._detect_and_process_capture(nb):
                    self.board[point] = EMPTY
                    return False
        block = self._block_of(point)
        if not self._has_liberty(block):
            self.board[point] = EMPTY
            return False
        self.board[point] = EMPTY
        return True

    def get_empty_points(self):
        return where1d(self.board == EMPTY)

    def row_start(self, row):
        return row * self.NS + 1

    def _initialize_empty_points(self, board):
        for row in range(1, self.size + 1):
            start = self.row_start(row)
            board[start : start + self.size] = EMPTY

    def _has_liberty(self, block: np.ndarray) -> bool:
        for stone in where1d(block):
            for nb in self.neighbors[stone]:
                if self.board[nb] == EMPTY:
                    return True
        return False

    def _block_of(self, stone):
        return self.connected_component(stone)

    def connected_component(self, point):
        marker = np.full(self.maxpoint, False, dtype=bool)
        pointstack = [point]
        color = self.get_color(point)
        marker[point] = True
        while pointstack:
            p = pointstack.pop()
            neighbors = self.neighbors_of_color(p, color)
            for nb in neighbors:
                if not marker[nb]:
                    marker[nb] = True
                    pointstack.append(nb)
        return marker

    def _detect_and_process_capture(self, nb_point):
        opp_block = self._block_of(nb_point)
        return not self._has_liberty(opp_block)

    def play_move(self, point, color):
        if point == PASS:
            return False
        elif self.board[point] != EMPTY:
            return False

        opp_color = opponent(color)
        self.board[point] = color
        neighbors = self.neighbors[point]
        for nb in neighbors:
            if self.board[nb] == opp_color:
                captured = self._detect_and_process_capture(nb)
                if captured:
                    self.board[point] = EMPTY
                    return False

        block = self._block_of(point)
        if not self._has_liberty(block):
            self.board[point] = EMPTY
            return False

        self.current_player = opponent(color)
        return True

    def neighbors_of_color(self, point, color):
        nbc = []
        for nb in self.neighbors[point]:
            if self.get_color(nb) == color:
                nbc.append(nb)
        return nbc

    def _neighbors(self, point):
        return [point - 1, point + 1, point - self.NS, point + self.NS]

    def _diag_neighbors(self, point):
        return [
            point - self.NS - 1,
            point - self.NS + 1,
            point + self.NS - 1,
            point + self.NS + 1,
        ]
