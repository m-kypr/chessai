from flask import Response
from state import State
import chess.svg
from flask import request, Flask, render_template, Markup
import chess
import tensorflow as tf


class Evaluator():
    def __init__(self):
        self.model = tf.keras.models.load_model('model/net')

    def __call__(self, s):
        s = s.serialize()[None]
        s = tf.convert_to_tensor(s)
        return self.model.predict(s)


class ClassicValuator():
    values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0
    }

    def __init__(self, ):
        super().__init__()

    pass


def explore_leaves(s, v):
    ret = []
    for e in s.edges():
        s.board.push(e)
        # print(e, v(s))
        ret.append((v(s), e))
        s.board.pop()
    return ret


app = Flask(__name__)
s = State()
e = Evaluator()


def ai_move():
    move = sorted(explore_leaves(s, e),
                  key=lambda x: x[0], reverse=s.board.turn)[0]
    print(move)
    s.board.push(move[1])


@app.route("/board.svg")
def board():
    return Response(chess.svg.board(board=s.board), mimetype='image/svg+xml')


@app.route("/move")
def move():
    if not s.board.is_game_over():
        move = request.args.get('move', default="")
        if move is not None and move != "":
            print("human moves", move)
            s.board.push_san(move)
            ai_move()
    else:
        print("GAME IS OVER")
    return hello_world()


def board_to_game(board):
    import chess.pgn
    game = chess.pgn.Game()
    import collections
    # undo all moves
    switchyard = collections.deque()
    while board.move_stack:
        switchyard.append(board.pop())

    game.setup(board)
    node = game

    # Replay all moves
    while switchyard:
        move = switchyard.pop()
        node = node.add_variation(move)
        board.push(move)

    game.headers["Result"] = board.result()
    return game


@app.route('/')
def hello_world():
    return render_template('yoink.html', fen=s.board.board_fen(), pgn=str(board_to_game(s.board).mainline_moves()))


if __name__ == "__main__":
    app.run(debug=True)
