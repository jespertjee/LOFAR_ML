import pandas as pd
from astropy.table import Table

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
    data = open_fits("../../Data/Best&Heckman/Best&Heckman2012.fit")

    names = data['SimbadName']

    # Fixing the source name column, since it is currently saved in bytes and should become a string
    names = names.apply(lambda s: s.decode('utf-8'))

    names.to_csv("../../Data/Best&Heckman/SDSS_names.txt", index=False)