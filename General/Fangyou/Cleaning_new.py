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
    # Opening file which has source_name to classification and some other info we might use for classification
    source_to_info = pd.read_csv("../../Data/Philip_data/Cleaned/Combined_secure_class.csv")
    source_to_info = source_to_info[["Source_Name", "AGN_final", "RadioAGN_final", "Classification"]]

    # Opening raw data and matching it to source
    data = []

    file_locations = [
        '../../Data/Fangyou_data/Original/Radio/Cross_match/bootes_final_cross_match_catalogue-v0.8.fits',
        '../../Data/Fangyou_data/Original/Radio/Cross_match/en1_final_cross_match_catalogue-v0.8.fits',
        '../../Data/Fangyou_data/Original/Radio/Cross_match/lockman_final_cross_match_catalogue-v0.8.fits']
    save_locations = [
        '../../Data/Fangyou_data/Cleaned/Complete_Bootes_clean.csv',
        '../../Data/Fangyou_data/Cleaned/Complete_Elais-N1_clean.csv',
        '../../Data/Fangyou_data/Cleaned/Complete_Lockman_clean.csv'
    ]
    for file, save_location in zip(file_locations, save_locations):
        dat = open_fits(file)
        #dat = dat.drop(columns=["help_id", "RA_HELP", "DEC_HELP", "OBJID", "ID_OPTICAL", "ID_SPITZER",
         #                       "ID", "stellar_type"])
        dat = dat.drop(columns=["Renamed_from"])

        # Changing column to strings instead of bytes
        dat['S_Code'] = dat['S_Code'].apply(lambda s: s.decode('utf-8'))
        dat['Created'] = dat['Created'].apply(lambda s: s.decode('utf-8'))
        dat['Position_from'] = dat['Position_from'].apply(lambda s: s.decode('utf-8'))

        # Have to do this weird thing since nan's are floats and else it will complain
        dat['stellar_type'] = dat['stellar_type'].fillna(b'')
        dat['stellar_type'] = dat['stellar_type'].apply(lambda s: s.decode('utf-8'))

        # Fixing the source name column, since it is currently saved in bytes and should become a string
        dat['Source_Name'] = dat['Source_Name'].apply(lambda s: s.decode('utf-8'))
        dat = dat.merge(source_to_info, on='Source_Name')
        data.append(data)

        # Saving data
        dat.to_csv(save_location, index=False)
