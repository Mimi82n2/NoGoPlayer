#!/usr/local/bin/python3
# /usr/bin/python3
# Set the path to your python3 above

#!/usr/bin/python3
# Set the path to your python3 above
from gtp_connection import GtpConnection
from board_base import DEFAULT_SIZE, GO_POINT, GO_COLOR
from board import GoBoard
from board_util import GoBoardUtil
from engine import GoEngine
import numpy as np
class NoGo:
    def __init__(self):
        GoEngine.__init__(self, "NoGo4", 1.0)
        self.name = "UCB"
        self.version = 1.0
        self.sim = 10000
        self.C = 0.4
        self.best_move = None

    def get_move(self, board: GoBoard, color: GO_COLOR) -> GO_POINT:
        return GoBoardUtil.generate_random_move(board, color)

    def set_sim_num(self, new_num):
        self.sim = new_num
    
    def get_best_move(self):
        return self.best_move

    def compute_ucb(self, num, val, N):
        return val/num + self.C*np.sqrt(np.log(N)/num)

    def select(self, stats, N):
        max_val = 0
        max_index = 0
        for index, (num, val) in enumerate(stats):
            if num == 0:
                return index
            ucb = self.compute_ucb(num, val, N)
            if ucb > max_val:
                max_val = ucb
                max_index = index
        return max_index
            
    def simulate(self, board:GoBoard, move, toplay):
        cboard = board.copy()
        cboard.play_move(move, toplay)
        return play_game(cboard)
    
    def run_ucb(self, board:GoBoard, moves, color):
        total_sim = self.sim*len(moves)
        stats = np.zeros((len(moves),2))

        for N in range(1, total_sim+1):
            index = self.select(stats, N)
            move = moves[index]
            winner = self.simulate(board, move, color)
            if winner == color:
                stats[index] += 1
            else:
                stats[index][0] += 1
            max_index = np.argmax(stats,axis=0)[0]
            self.best_move = moves[max_index]
        return self.best_move

    def get_move_ucb(self, board:GoBoard, color:int):
        cboard = board.copy()
        cboard.current_player = color
        moves = GoBoardUtil.generate_legal_moves(cboard, color)
        if not moves:
            return None
        elif len(moves) == 1:
            return moves[0]
        else:
            best = self.run_ucb(board, moves, color)
            return best
def play_game(board:GoBoard):
    while True:
        color = board.current_player
        move = GoBoardUtil.generate_random_move(board,color)
        board.play_move(move, color)
        if move is None:
            break
    winner = GoBoardUtil.opponent(color)
    return winner
def run() -> None:
    board: GoBoard = GoBoard(DEFAULT_SIZE)
    con: GtpConnection = GtpConnection(NoGo(), board)
    con.start_connection()
if __name__ == "__main__":
    run()
