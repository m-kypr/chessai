## machine learning powered chess engine 
bitboard representation
State:
* ALL:
** Blank
** en passant
=> 2 
* pieces:
** Pawn 
** Queen
** King 
** Rook
** Bishop
** Knight
=> 6x2 = 12

==> 14

board size    
8x8         x  7  +1 =  449 bits 

using this: https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation

rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1

