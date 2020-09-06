import chess
import numpy as np


class State():

    dd = {'P': 1, 'N': 2, 'B': 3, 'R': 4, 'Q': 5, 'K': 6,
          'p': 7, 'n': 8, 'b': 9, 'r': 10, 'q': 11, 'k': 12}

    def __init__(self, board=None):
        if board:
            self.board = board
        else:
            self.board = chess.Board()

    def edges(self):
        return list(self.board.legal_moves)

    def serialize(self):
        boardstate = np.zeros(64, np.uint8)
        for i in range(64):
            piece = self.board.piece_at(i)
            if piece:
                boardstate[i] = self.dd[piece.symbol()]
#         if self.board.has_castling_rights(chess.WHITE):
#             assert boardstate[0] == dd['R']
#             boardstate[0] == 13
#         if self.board.has_castling_rights(chess.BLACK):
#             assert boardstate[63] == dd['r']
#             boardstate[63] == 13
        if self.board.ep_square:
            assert boardstate[self.board.ep_square] == 0  # is blank
            boardstate[self.board.ep_square] = 13
        boardstate = boardstate.reshape(8, 8)

        state = np.zeros((5, 8, 8), np.uint8)

#         print(boardstate)
        # 0-3 columns to binary
        # I still dont completly understand what We are doing here
        state[0] = (boardstate >> 3) & 1
        state[1] = (boardstate >> 2) & 1
        state[2] = (boardstate >> 1) & 1
        state[3] = (boardstate >> 0) & 1

        # 4th turn, castling rights
        qsw = self.board.has_queenside_castling_rights(chess.WHITE)
        qsb = self.board.has_queenside_castling_rights(chess.BLACK)
        ksw = self.board.has_kingside_castling_rights(chess.WHITE)
        ksb = self.board.has_queenside_castling_rights(chess.BLACK)
        state[4] = (self.board.turn, qsw, qsb, ksw, ksb, 0, 0, 0)

        return state
