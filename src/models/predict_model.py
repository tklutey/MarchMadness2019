import matplotlib.pyplot as plt
import pandas as pd
from tensorflow.keras.models import model_from_json
from util import split_dataset
from util.IntermediateFilePersistence import IntermediateFilePersistence

def __read_from_csv_and_split():
    fp = IntermediateFilePersistence('NormalizedFeatureData.csv')
    df = fp.read_from_csv()

    return split_dataset.split_training_data_randomly_with_seed(df, 0)
    
def __load_model():
    # load json and create model
    json_file = open('/Users/kluteytk/development/projects/MarchMadness2019/models/model_architecture.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights('/Users/kluteytk/development/projects/MarchMadness2019/models/model_weights.h5')
    print("Loaded model from disk")
    return loaded_model

def __actual_vs_predicted(predictions, test_labels):
    test_labels = test_labels.reset_index(drop=True)

    df_eval = pd.DataFrame()
    df_eval['Predicted'] = predictions
    df_eval['Actual'] = test_labels
    
    return df_eval
    
def __sign(x):
    return 1 - (x<=0)
    
def __print_hit_rate(df_eval):
    correct = 0
    incorrect = 0
    points_off = 0

    for i,r in df_eval.iterrows():
        points_off = abs(r['Predicted'] - r['Actual']) + points_off
        if __sign(r['Predicted']) == __sign(r['Actual']):
            correct = correct + 1
        else:
            incorrect = incorrect + 1
        
    total_games = correct+incorrect
    hit_rate = correct / total_games
    err_per_game = points_off / total_games
    print('Total Games: ' + str(total_games))
    print('Hit rate: ' + '{:.1%}'.format(hit_rate))
    print('Points off per game: ' + str(err_per_game))


def __plot_predictions(predictions, test_labels):  
    plt.figure()
    plt.scatter(test_labels, predictions)
    plt.xlabel('True Values [ScoreDiff]')
    plt.ylabel('Predictions [ScoreDiff]')
    plt.axis('equal')
    plt.axis('square')
    _ = plt.plot([-50, 50], [-50, 50])


def predict(test_dataset=None):
    
    model = __load_model()

    if test_dataset is None:
        (_, _), (test_dataset, _) = __read_from_csv_and_split()
    
    test_predictions = model.predict(test_dataset).flatten()
    
    return test_predictions


def evaluate_predictions(predictions, test_labels):
    df_eval = __actual_vs_predicted(predictions, test_labels)
    print(df_eval.head())
    __plot_predictions(predictions, test_labels)
    __print_hit_rate(df_eval)


if __name__ == '__main__':
    (train_dataset, train_labels), (test_dataset, test_labels) = __read_from_csv_and_split()
    predictions = predict()
    evaluate_predictions(predictions, test_labels)    
