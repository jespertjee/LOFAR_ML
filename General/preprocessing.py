from astropy.table import Table
import pandas as pd


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


if __name__ == "__main__":
    data = []

    # Opening all the data and converting it to a pandas dataframe
    file_locations = ['../Data/AGNclasses_Bootes_v1.fits', '../Data/AGNclasses_Lockman_v1.fits',
                      '../Data/AGNclasses_ElaisN1_v1.fits']
    for file in file_locations:
        data.append(open_fits(file))

    # All locations, adding data about
    all_locations = ['Bootes', 'Lockman', 'ElaisN1']
    for i, location in enumerate(all_locations):
        data[i] = add_location_column(data[i], all_locations, location)

    # Saving data as csv
    file_locations_csv = ['../Data/AGNclasses_Bootes_v1.csv', '../Data/AGNclasses_Lockman_v1.csv',
                          '../Data/AGNclasses_ElaisN1_v1.csv']
    for df, file_name in zip(data, file_locations_csv):
        df.to_csv(file_name, index=False)

    # Combining all the data into one table and saving it as a csv
    combined = pd.concat(data)
    combined.to_csv('../Data/Combined.csv', index=False)

