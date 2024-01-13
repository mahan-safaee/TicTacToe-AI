import itertools
import numpy as np


class Board:
    def __init__(self, size: int, emp=" "):
        self.EMP = emp
        self.mat = np.full((size, size), self.EMP, dtype="<U1")
        self.size: int = size

    def __getitem__(self, n):
        return self.mat[n]

    def __setitem__(self, key, value):
        self.mat[key] = value

    def __repr__(self):
        return str(self.mat)

    def check_win(self, player):
        ev = self.mat == player
        return (
            np.any(np.all(ev, axis=0))
            or np.any(np.all(ev, axis=1))
            or np.all(np.diag(ev))
            or np.all(np.diag(ev[:, ::-1]))
        )

    def check_draw(self):
        return np.all(self.mat.flat != self.EMP)

    def check_gameover(self, p1, p2):
        res = False
        if res := self.check_win(p1):
            print(p1, "won!")
        elif res := self.check_win(p2):
            print(p2, "won!")
        elif res := self.check_draw():
            print("Draw!")
        return res

    def minimax(self, p1, p2, maxx) -> float:
        if self.check_win(p1):
            return 1
        if self.check_draw():
            return 0
        if self.check_win(p2):
            return -1
        best_score: float = float("-inf")
        for pos in itertools.product(range(self.size), repeat=2):
            if self[pos] != self.EMP:
                continue
            if best_score >= maxx:
                return best_score
            self[pos] = p1
            subscore: float = -self.minimax(p2, p1, -best_score)
            self[pos] = self.EMP
            if subscore > best_score:
                best_score = subscore
        return best_score

    def find_move(self, p1, p2) -> tuple[int, int]:
        best_score: float = float("-inf")
        for pos in itertools.product(range(self.size), repeat=2):
            if self[pos] != self.EMP:
                continue
            self[pos] = p1
            subscore: float = -self.minimax(p2, p1, -best_score)
            self[pos] = self.EMP
            if subscore > best_score:
                index: tuple[int, int] = pos
                best_score = subscore
        return index

    def make_move(self, p1, p2):
        self[self.find_move(p1, p2)] = p1

    def X(self, X, O):
        print("Play move:")
        while move := tuple(map(int, input().strip().split())):
            if self[move] == self.EMP:
                break
            print("again ", end="")
        self[move] = X

    def O(self, X, O):
        self.make_move(O, X)


def play_game():
    board = Board(3)
    while True:
        match input("X or O? ").lower():
            case "x":
                xof, xo = [Board.X, Board.O], "XO"
                break
            case "o":
                xof, xo = [Board.O, Board.X], "OX"
                break
    print(board)
    while True:
        for f in xof:
            f(board, *xo)
            print(board)
            if board.check_gameover(*xo):
                return


if __name__ == "__main__":
    while True:
        play_game()
        print("q for Quit, else for play again")
        if input().lower() == "q":
            break
