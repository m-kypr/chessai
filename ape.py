import os
import chess.pgn
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, Sequential

dataset_dir = "E:\\Datasets\\kaggle_chess\\"
dataset_dir = os.path.join(dataset_dir)
dataset_file = os.path.join(
    dataset_dir, 'all_with_filtered_anotations_since1998.txt')
chess_pickle = os.path.join(dataset_dir, 'games.pickle')


def prepare_dataset():
    open(chess_pickle, 'w+')
    with open(dataset_file, 'r') as f:
        games = []
        for game_string in f.read().split('\n')[5:-2]:
            game = chess.pgn.read_game(game_string.split("###")[1])
            games.append(game)
            print(game, file=open(chess_pickle, 'a'), end='\n\n')

    return games


def build_model():
    model = Sequential(name='seqential')
    model.add(keras.Input(shape=(250, 250, 3)))
    model.add(layers.Dense(2, activation='relu', name='layer1'))
    model.add(layers.Dense(3, activation='relu', name='layer2'))
    model.add(layers.Dense(4, name='layer3'))

    x = tf.ones((1, 250, 250, 3))
    y = model(x)

    print(model.summary())


if __name__ == "__main__":
    # build_model()
    pass
