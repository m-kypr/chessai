import chess


class State():
    def __init__(self, board=None):
        if board:
            self.board = board
        else:
            self.board = chess.Board()

    def serialize(self):
        # convert board into bitboard of 449 bits (readme)

        for i in range(64):
            piece = self.board.piece_at(i)
            piece.piece_type


# have a look at this :  https://github.com/geohot/twitchchess/blob/master/state.py
# continue later feeling stupid and braindead rn but im learning
