from astropy.table import Table
import pandas as pd
import numpy as np
""""
Purpose of this file is to clean the data up, this file should not be confused with preprocessing, since preprocessing
techniques can influence the ML algorithm. While the purpose of this file is simply cleaning the files, adding 
necessary columns (optical ID and redshift). It produces various output files which are various stages of cleaning up
the data
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


def add_location_column(data: pd.DataFrame, all_locations, location: str):
    """"
    Add additional columns to pandas dataframe that show that the location of the radio sources are. This new data is
    one-hot encoded
    
    :param data: pandas dataframe containing the data
    :param all_locations: all possible locations in the dataset
    :param location: the location the data is in
    """
    data[all_locations] = 0
    data[location] = 1
    return data


def create_classification(row):
    """"
    The classification is currently given by 2 columns AGN_final, RadioAGN_final, this simply creates a single column
    for it, the classification works as follows

    AGN_final=0  &  RadioAGN_final=0     -> star-forming galaxy
    AGN_final=1  &  RadioAGN_final=0     -> 'radio-quiet' AGN
    AGN_final=0  &  RadioAGN_final=1     -> 'jet-mode' radio AGN / low-excitation radio galaxy
    AGN_final=1  &  RadioAGN_final=1     -> quasar-like radio AGN / high-excitation radio galaxy
    AGN_final=-1 or RadioAGN_final=-1    -> no secure classification

    non-secure classifications have already been removed.

    :param row: row containing data
    """
    if row['AGN_final'] == 0 and row['RadioAGN_final'] == 0:
        return 'star-forming galaxy'
    elif row['AGN_final'] == 1 and row['RadioAGN_final'] == 0:
        return 'radio-quiet AGN'
    elif row['AGN_final'] == 0 and row['RadioAGN_final'] == 1:
        return 'jet-mode radio AGN/low-excitation radio galaxy'
    elif row['AGN_final'] == 1 and row['RadioAGN_final'] == 1:
        return 'quasar-like radio AGN / high-excitation radio galaxy'


if __name__ == "__main__":
    data = []

    # Opening all the data and converting it to a pandas dataframe
    file_locations = ['../../Data/Philip_data/AGNclasses_Bootes_v1.fits',
                      '../../Data/Philip_data/AGNclasses_Lockman_v1.fits',
                      '../../Data/Philip_data/AGNclasses_ElaisN1_v1.fits']
    for file in file_locations:
        data.append(open_fits(file))

    # Fixing the source name column, since it is currently saved in bytes and should become a string
    for i in range(len(data)):
        data[i]['Source_Name'] = data[i]['Source_Name'].apply(lambda s: s.decode('utf-8'))

    # All locations, adding data about which region the data is from
    all_locations = ['Bootes', 'Lockman', 'ElaisN1']
    for i, location in enumerate(all_locations):
        data[i] = add_location_column(data[i], all_locations, location)

    # Adding Optical ID's so we can add redshifts
    Source_Name_to_optical_ID = pd.read_csv('../../Data/Philip_data/ID_cross_matching/Source_Name_to_optical_ID.csv')
    pd.options.mode.chained_assignment = None
    # Columns which will replace some of their nan's, this has to be done since the source often uses -1 or -99 as nan
    columns_negative_one_to_nan = ['Donley', 'Lacy', 'Stern', 'Messias', 'KI', 'Ch2_Ch4', 'Ch4_24mu']
    columns_negative_99_to_nan = ['Xray', 'Opt_spec', 'AGNfrac_af', 'AGNfrac_af_16', 'AGNfrac_cg_s', 'AGNfrac_cg_s_16',
                                  'AGNfrac_cg_f', 'AGNfrac_cg_f_16', 'Chi_sq_MpBp', 'Chi_sq_AfCg', 'Mass_conc',
                                  'SFR_conc', 'Radio_excess', 'Radio_excess_DJS', 'Extended_radio']
    for i in range(len(data)):
        data[i] = pd.merge(data[i], Source_Name_to_optical_ID, on='Source_Name')

        # removing any -99 or -999 in the cross-identification
        data[i]['IDOptical'][data[i]['IDOptical'] == '-99'] = np.nan
        data[i]['IDOptical'][data[i]['IDOptical'] == '-999'] = np.nan

        data[i]['IDSpitzer'][data[i]['IDSpitzer'] == '-99'] = np.nan
        data[i]['IDSpitzer'][data[i]['IDSpitzer'] == '-999'] = np.nan

        # Removing -1 (data not sufficient/too low S/N) in the Donley, Lacy, Stern, Messias, KI, Ch2_Ch4, Ch4_24mu
        data[i][columns_negative_one_to_nan] = data[i][columns_negative_one_to_nan].replace(-1, np.nan)

        # Removing -99 (data doesn't exist) in the Xray, Opt_spec, AGNfrac_af, AGNfrac_af_16, AGNfrac_cg_s,
        # AGNfrac_cg_s_16, AGNfrac_cg_f, AGNfrac_cg_f_16, Chi_sq_MpBp, Chi_sq_AfCg, Mass_conc, SFR_conc,
        # Radio_excess, Radio_excess_DJS, Extended_radio columns
        data[i][columns_negative_99_to_nan] = data[i][columns_negative_99_to_nan].replace(-99, np.nan)

        # Adding new column with classification
        data[i]['Classification'] = data[i].apply(create_classification, axis=1)

    # Saving data as csv
    file_locations_csv = ['../../Data/Philip_data/Cleaned/AGNclasses_Bootes_v1.csv',
                          '../../Data/Philip_data/Cleaned/AGNclasses_Lockman_v1.csv',
                          '../../Data/Philip_data/Cleaned/AGNclasses_ElaisN1_v1.csv']
    for df, file_name in zip(data, file_locations_csv):
        df.to_csv(file_name, index=False)

    # Combining all the data into one table and saving it as a csv
    combined = pd.concat(data)
    combined.to_csv('../../Data/Philip_data/Cleaned/Combined.csv', index=False)

    # Also saving a version of combined where we drop the columns with no clear classification
    combined_secure_class = combined[combined['AGN_final'] != -1]
    combined_secure_class = combined_secure_class[combined_secure_class['RadioAGN_final'] != -1]

    combined_secure_class.to_csv('../../Data/Philip_data/Cleaned/Combined_secure_class.csv', index=False)

