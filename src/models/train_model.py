import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
import pandas as pd
from util import split_dataset
from util.IntermediateFilePersistence import IntermediateFilePersistence

EPOCHS = 10000

class PrintDot(keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs):
    if epoch % 100 == 0: print('')
    print('.', end='')

def build_model(df_training_data):
    model = keras.Sequential([
        layers.Dense(500, activation=tf.nn.relu, input_shape=[len(df_training_data.keys())]),
        layers.Dense(250, activation=tf.nn.relu),
        layers.Dense(50, activation=tf.nn.relu),
        layers.Dense(1)
      ])
    
    optimizer = tf.train.AdamOptimizer(0.00001)

    model.compile(loss='mse',
            optimizer=optimizer,
            metrics=['mae', 'mse'])
    
    return model

def train_model(model, df_training_data, df_training_labels):
    early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)

    history = model.fit(df_training_data, df_training_labels, epochs=EPOCHS,
                    validation_split = 0.2, verbose=0, callbacks=[early_stop, PrintDot()])
    
    hist = pd.DataFrame(history.history)
    hist['epoch'] = history.epoch
    
    scores = model.evaluate(df_training_data, df_training_labels, verbose=0)
    print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
    
    return model, hist

def plot_training(hist):
    plt.figure()
    plt.xlabel('Epoch')
    plt.ylabel('Mean Abs Error [ScoreDiff]')
    plt.plot(hist['epoch'], hist['mean_absolute_error'],
           label='Train Error')
    plt.plot(hist['epoch'], hist['val_mean_absolute_error'],
           label = 'Val Error')
    plt.legend()
    plt.ylim([0,10])
    
    plt.figure()
    plt.xlabel('Epoch')
    plt.ylabel('Mean Square Error [$ScoreDiff^2$]')
    plt.plot(hist['epoch'], hist['mean_squared_error'],
           label='Train Error')
    plt.plot(hist['epoch'], hist['val_mean_squared_error'],
           label = 'Val Error')
    plt.legend()
    plt.ylim([0,200])
    
def make(train_dataset=None, train_labels=None):
    if train_dataset is None:
        fp = IntermediateFilePersistence('NormalizedFeatureData.csv')
        df = fp.read_from_csv()
        (train_dataset, train_labels), (_, _) = split_dataset.split_training_data_randomly_with_seed(df)

    model = build_model(train_dataset)
    model, hist = train_model(model, train_dataset, train_labels)
    
    plot_training(hist)
    
    return model
    
def persist(model):
    model_architecture = '/Users/kluteytk/development/projects/MarchMadness2019/models/model_architecture.json'
    model_weights = '/Users/kluteytk/development/projects/MarchMadness2019/models/model_weights.h5'
    model_json = model.to_json()
    with open(model_architecture, "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights(model_weights)
    print("Saved model to disk")
    
    
if __name__ == '__main__':    
    model = make()
    persist(model)