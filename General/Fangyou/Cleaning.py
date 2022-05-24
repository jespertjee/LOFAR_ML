from astropy.table import Table
import pandas as pd
import numpy as np
""""
Purpose of this file is to clean the data up, and particularly add classifications and remove data without any 
classifications. No missing rows/columns are fixed here, that is done in preprocessing.
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
    # Opening file which has source_name to classification
    source_to_class = pd.read_csv("../../Data/Philip_data/Cleaned/Combined_secure_class.csv")
    source_to_class = source_to_class[["Source_Name", "Classification"]]

    # Opening raw data and matching it to source
    data = []

    file_locations = [
        '../../Data/Fangyou_data/Original/Raw/Bootes_sedfit_v1.0.fits',
        '../../Data/Fangyou_data/Original/Raw/EN1_sedfit_v1.0.fits',
        '../../Data/Fangyou_data/Original/Raw/LH_sedfit_v1.0.fits']
    save_locations = [
        '../../Data/Fangyou_data/Cleaned/Bootes_clean.csv',
        '../../Data/Fangyou_data/Cleaned/Elais-N1_clean.csv',
        '../../Data/Fangyou_data/Cleaned/Lockman_clean.csv'
    ]
    for file, save_location in zip(file_locations, save_locations):
        dat = open_fits(file)
        dat = dat.drop(columns=["ID", "radioID"])

        # Fixing the source name column, since it is currently saved in bytes and should become a string
        dat['Source_Name'] = dat['Source_Name'].apply(lambda s: s.decode('utf-8'))
        dat = dat.merge(source_to_class, on='Source_Name')
        data.append(data)

        # Saving data
        dat.to_csv(save_location, index=False)
