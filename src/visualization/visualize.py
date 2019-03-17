from util import split_dataset
from util.BaseFilePersistence import BaseFilePersistence
from util.IntermediateFilePersistence import IntermediateFilePersistence

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from string import ascii_letters

def visualize_corr(df):
    sns.set(style="white")

    # Compute the correlation matrix
    corr = df.corr()

    # Generate a mask for the upper triangle
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True

    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(11, 9))

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(220, 10, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5})


def test_corr(df):
    df_corr = df.corr()
    fp = BaseFilePersistence('/Users/kluteytk/development/projects/MarchMadness2019/data/experiment/Correlations.csv')
    fp.write_to_csv(df_corr, index=True)
    print(df_corr)

def random_forest(df):
    (train_dataset, train_labels), (test_dataset, test_labels) = split_dataset.split_training_data_randomly_with_seed(
        df)

    model = RandomForestRegressor(random_state=1, max_depth=10)
    df = pd.get_dummies(df)
    model.fit(train_dataset, train_labels)

    features = df.columns
    importances = model.feature_importances_
    imp = pd.DataFrame(importances)
    imp['Feat'] = features[imp.index]
    fp = BaseFilePersistence('/Users/kluteytk/development/projects/MarchMadness2019/data/experiment/FeatureImportance.csv')
    fp.write_to_csv(imp, index=False)
    indices = np.argsort(importances)[-20:]  # top 10 features
    plt.title('Feature Importances')
    plt.barh(range(len(indices)), importances[indices], color='b', align='center')
    plt.yticks(range(len(indices)), [features[i] for i in indices])
    plt.xlabel('Relative Importance')
    plt.show()

if __name__ == '__main__':
    fr = IntermediateFilePersistence('NormalizedFeatureData.csv')
    df = fr.read_from_csv()
    test_corr(df)