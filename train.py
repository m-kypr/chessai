import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import matplotlib.pyplot as plt
import os


def make_dataset(path):
    with np.load(path) as data:
        trainX, valX, testX = np.split(
            data['arr_0'], [int(len(data['arr_0'])*0.8), int(len(data['arr_0'])*0.9)])
        trainY, valY, testY = np.split(
            data['arr_1'], [int(len(data['arr_1'])*0.8), int(len(data['arr_1'])*0.9)])

        print(trainY.shape, valY.shape, testY.shape)
        train_dataset = tf.data.Dataset.from_tensor_slices(
            (trainX, trainY))
        test_dataset = tf.data.Dataset.from_tensor_slices(
            (testX, testY))
        val_dataset = tf.data.Dataset.from_tensor_slices(
            (valX, valY))

        return trainX, trainY, testX, testY, train_dataset, test_dataset, val_dataset


def make_dataset2(path):
    with np.load(path) as data:
        trainX = data['arr_0']
        trainY = data['arr_1']
        return trainX, trainY, tf.data.Dataset.from_tensor_slices(
            (trainX, trainY))


def build_model():
    model = keras.Sequential(name='seqential')

    model.add(layers.Conv2D(32, (2, 2), activation='relu', input_shape=(5, 8, 8)))
    model.add(layers.Conv2D(32, (2, 2), activation='relu', padding='same'))
    model.add(layers.Conv2D(32, (2, 2), activation='relu'))
    # model.add(layers.MaxPooling2D((1, 1)))
    model.add(layers.Conv2D(64, (2, 2), activation='relu', padding='same'))
    model.add(layers.Conv2D(64, (2, 2), activation='relu', padding='same'))
    model.add(layers.Conv2D(64, (2, 2), activation='relu'))
    # model.add(layers.MaxPooling2D((1, 1)))
    model.add(layers.Conv2D(128, (2, 2), activation='relu', padding='same'))
    model.add(layers.Conv2D(128, (2, 2), activation='relu', padding='same'))
    model.add(layers.Conv2D(128, (2, 2), activation='relu'))
    model.add(layers.Flatten())
    model.add(layers.Dense(1, activation='tanh'))

    print(model.summary())

    model.compile(optimizer='adam',
                  loss=tf.losses.MeanSquaredError(), metrics=tf.metrics.MeanSquaredError())
    return model


if __name__ == "__main__":
    from dataset import dataset_dir
    tx, ty, tds = make_dataset2(
        os.path.join(dataset_dir, 'dataset_1k.npz'))
    model = build_model()
    history = model.fit(tx, ty, epochs=100, validation_split=0.1,
                        shuffle=True, batch_size=256)
    model.save('model/net')
    # model = tf.saved_model.load('model/net')
    plt.plot(history.history['loss'], label='loss')
    plt.ylim([0, 1])
    plt.show()

    # test_loss, test_acc = model.evaluate(tx,  ty, verbose=2)
