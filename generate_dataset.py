import os
import chess
import chess.pgn
import numpy as np
from state import State


def generate_dataset(num, d):
    X, Y = [], []
    values = {'1/2-1/2': 0, '0-1': -1, '1-0': 1}
    c = 0
    for game_file in os.listdir(d):
        game_path = open(os.path.join(d, game_file))
        while True:
            game = chess.pgn.read_game(game_path)
            if not game:
                break
            res = game.headers['Result']
            if res not in values:
                continue
            value = values[res]
            board = game.board()
            for move in game.mainline_moves():
                board.push(move)
                ser = State(board).serialize()
                X.append(ser)
                Y.append(value)
            if c % 100 == 0:
                print(f"parsing game {c}, got {len(X)} examples")
            if num is not None and len(X) > num:
                return np.array(X), np.array(Y)
            c += 1
    X = np.array(X)
    Y = np.array(Y)
    return X, Y


if __name__ == "__main__":
    from dataset import dataset_dir
    from time import time
    X, Y = generate_dataset(25000000, d=os.path.join(
        dataset_dir, 'kaggle_pgn_ALL'))
    np.savez_compressed(os.path.join(dataset_dir, 'dataset_25M.npz'), X, Y)
