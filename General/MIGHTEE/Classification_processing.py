import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.linear_model import LinearRegression

"""
Purpose of this file is to preprocess the classification.txt file, mostly to make the classifications actually appear
"""

def create_classification(row):
    """"
    :param row: row containing data
    """
    if row['SFG'] or row['probSFG']:
        return 'star-forming galaxy'
    elif row['RQAGN']:
        return 'radio-quiet AGN'
    elif row['LERG'] or row['probLERG']:
        return 'jet-mode radio AGN/low-excitation radio galaxy'
    elif row['HERG']:
        return 'quasar-like radio AGN / high-excitation radio galaxy'
    elif row['unclass']:
        return np.nan

def create_classification_secure(row):
    """"
    :param row: row containing data
    """
    if row['SFG']:
        return 'star-forming galaxy'
    elif row['RQAGN']:
        return 'radio-quiet AGN'
    elif row['LERG']:
        return 'jet-mode radio AGN/low-excitation radio galaxy'
    elif row['HERG']:
        return 'quasar-like radio AGN / high-excitation radio galaxy'
    elif row['unclass']:
        return np.nan

if __name__ == "__main__":
    # Prob
    data = pd.read_csv('../../Data/MIGHTEE/Classification/Classification_less_columns_plus_SPeak.csv')

    # Adding classifications
    data['Classification'] = data.apply(create_classification, axis=1)
    data = data.drop(columns=['SFG', 'probSFG', 'RQAGN', 'LERG', 'probLERG', 'HERG', 'unclass'])

    # Converting to uJy
    data[['S_INT14', 'S_PEAK14']] *= 10**6

    data.to_csv("../../Data/MIGHTEE/Classification/Classification_less_columns_preprocessed.csv", index=False)

    # Secure
    data = pd.read_csv('../../Data/MIGHTEE/Classification/Classification_less_columns_plus_SPeak.csv')

    # Adding classifications
    data['Classification'] = data.apply(create_classification_secure, axis=1)
    data = data.drop(columns=['SFG', 'probSFG', 'RQAGN', 'LERG', 'probLERG', 'HERG', 'unclass'])

    # Converting to uJy
    data[['S_INT14', 'S_PEAK14']] *= 10 ** 6

    data.to_csv("../../Data/MIGHTEE/Classification/Classification_less_columns_preprocessed_secure.csv", index=False)

