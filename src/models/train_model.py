import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
import pandas as pd
from features import build_features

EPOCHS = 1000

class PrintDot(keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs):
    if epoch % 100 == 0: print('')
    print('.', end='')

def build_model(df_training_data):
    model = keras.Sequential([
        layers.Dense(64, activation=tf.nn.relu, input_shape=[len(df_training_data.keys())]),
        layers.Dense(1)
      ])
    
    optimizer = tf.train.RMSPropOptimizer(0.001)

    model.compile(loss='mse',
            optimizer=optimizer,
            metrics=['mae', 'mse'])
    
    return model

def train_model(model, df_training_data, df_training_labels):
    early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=50)

    history = model.fit(df_training_data, df_training_labels, epochs=EPOCHS,
                    validation_split = 0.2, verbose=0, callbacks=[early_stop, PrintDot()])
    
    hist = pd.DataFrame(history.history)
    hist['epoch'] = history.epoch
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
    plt.ylim([0,5])

def create_train_model():
    (train_dataset, train_labels), (test_dataset, test_labels) = build_features.create_dataset()
    model = build_model(train_dataset)
    model, hist = train_model(model, train_dataset, train_labels)
    return model

def main():
    (train_dataset, train_labels), (test_dataset, test_labels) = build_features.create_dataset()
    model = build_model(train_dataset)
    model, hist = train_model(model, train_dataset, train_labels)
    print(hist.tail())
    plot_training(hist)
    
if __name__ == '__main__':
#    print(sys.path)

    main()
    