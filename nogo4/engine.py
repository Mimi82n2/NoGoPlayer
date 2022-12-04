from board_base import GO_POINT, NO_POINT
from board import GoBoard

DEFAULT_KOMI = 6.5

class GoEngine:
    def __init__(self, name: str, version: float) -> None:
        self.name: str = name
        self.version: float = version
        self.komi: float = DEFAULT_KOMI

    def get_move(self, board: GoBoard, color: int) -> GO_POINT:
        pass
        