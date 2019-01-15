import sys
sys.path.append('/Users/kluteytk/development/projects/march_madness/MarchMadness2019/src/')

import train_model
from features import build_features
import matplotlib.pyplot as plt
import pandas as pd

def predict(model, test_dataset):
    test_predictions = model.predict(test_dataset).flatten()
    return test_predictions

def plot_predictions(predictions, test_labels):    
    plt.scatter(test_labels, predictions)
    plt.xlabel('True Values [ScoreDiff]')
    plt.ylabel('Predictions [ScoreDiff]')
    plt.axis('equal')
    plt.axis('square')
    _ = plt.plot([-50, 50], [-50, 50])

    
def actual_vs_predicted(predictions, test_labels):
    test_labels = test_labels.reset_index(drop=True)

    df_eval = pd.DataFrame()
    df_eval['Predicted'] = predictions
    df_eval['Actual'] = test_labels
    
    return df_eval
    
def sign(x):
    return 1 - (x<=0)
    
def print_hit_rate(df_eval):
    correct = 0
    incorrect = 0
    points_off = 0

    for i,r in df_eval.iterrows():
        points_off = abs(r['Predicted'] - r['Actual']) + points_off
        if sign(r['Predicted']) == sign(r['Actual']):
            correct = correct + 1
        else:
            incorrect = incorrect + 1
        
    total_games = correct+incorrect
    hit_rate = correct / total_games
    err_per_game = points_off / total_games
    print('Total Games: ' + str(total_games))
    print('Hit rate: ' + '{:.1%}'.format(hit_rate))
    print('Points off per game: ' + str(err_per_game))
    

def main():
    (train_dataset, train_labels), (test_dataset, test_labels) = build_features.create_dataset()
    model = train_model.create_train_model()
    predictions = predict(model, test_dataset)
    df_eval = actual_vs_predicted(predictions, test_labels)
    print(df_eval)
    plot_predictions(predictions, test_labels)
    print_hit_rate(df_eval)
    


    
if __name__ == '__main__':
#    print(sys.path)
    
    main()