import numpy as np
from astropy.table import Table
import pandas as pd
from sklearn.impute import KNNImputer

"""
Purpose of this file is to preprocess the data. Useless columns will be dropped and values imputed, etc.
"""

def open_fits(filename: str):
    """"
    Open fits file and load it as a pandas dataframe

    :param filename: location of the fits file

    :returns: data, pandas dataframe
    """
    dat = Table.read(filename, format='fits')
    data = dat.to_pandas()

    return data


if __name__ == "__main__":
    # Opening file which has source_name to classification and some other info we might use for classification
    source_to_class = pd.read_csv("../../Data/Philip_data/Cleaned/Combined_secure_class.csv")
    source_to_class = source_to_class[["Source_Name", "AGN_final", "RadioAGN_final", "Classification",
                                       'Radio_excess', 'AGNfrac_af', 'AGNfrac_af_16', 'AGNfrac_cg_s_16']]

    # Opening raw data and matching it to source
    filled_data = []
    non_filled_data = []

    file_locations = [
        '../../Data/Fangyou_data/Original/Cigale_input/bootes_cigale.fits',
        '../../Data/Fangyou_data/Original/Cigale_input/en1_cigale.fits',
        '../../Data/Fangyou_data/Original/Cigale_input/lockman_cigale.fits']
    save_locations = [
        '../../Data/Fangyou_data/Cleaned/Bootes_preprocessed_cigale.csv',
        '../../Data/Fangyou_data/Cleaned/Elais-N1_preprocessed_cigale.csv',
        '../../Data/Fangyou_data/Cleaned/Lockman_preprocessed_cigale.csv'
    ]

    for i, file, save_location in zip([0,1,2], file_locations, save_locations):
        # Opening file
        dat = open_fits(file)

        # Columns to remove, namely the errors and the magnitudes (mag are simply conversions from flux,
        # so not interesting
        remove_columns_error = [column for column in dat.columns if 'err' in column.lower()]
        dat = dat.drop(columns=remove_columns_error)

        # Setting negative values to nan (later they should be set to the minimum
        dat_num = dat.select_dtypes(include=[float])
        dat[dat_num<0] = np.nan

        # Fixing the source name column, since it is currently saved in bytes and should become a string
        dat['id'] = dat['id'].apply(lambda s: s.decode('utf-8'))
        dat = dat.merge(source_to_class, left_on='id', right_on='Source_Name')

        dat.to_csv(save_location, index=False)



