import pandas as pd
from Get_SDSS_names import open_fits
import numpy as np
from astropy.io import ascii
from astropy.table import QTable

def create_classification(row):
    """"
    The classification is currently given by 3 columns A, L, and H, this simply creates a single column
    for it, the classification works as follows

    A=0             -> star-forming galaxy
    A=1  &  L=1     -> 'jet-mode' radio AGN / low-excitation radio galaxy
    A=1  &  H=1     -> quasar-like radio AGN / high-excitation radio galaxy

    :param row: row containing data
    """
    if row['A'] == 0 :
        return 'star-forming galaxy'
    elif row['A'] == 1:
        if row['L'] == 1:
            return 'jet-mode radio AGN/low-excitation radio galaxy'
        elif row['H'] == 1:
            return 'quasar-like radio AGN / high-excitation radio galaxy'
    return 'Radio-loud AGN'


def asinh_mag_to_flux_density(mag, f0, b):
    return 2 * b * f0 * np.arcsinh(mag/(-2.5/np.log(10)) - np.log(b))


if __name__ == "__main__":
    BestHeckman = open_fits("../../Data/Best&Heckman/Best&Heckman2012.fit")
    SDSS = pd.read_csv("../../Data/Best&Heckman/SDSS.csv")

    # Fixing the source name column, since it is currently saved in bytes and should become a string
    BestHeckman['SimbadName'] = BestHeckman['SimbadName'].apply(lambda s: s.decode('utf-8')).str[0:-1]

    data = BestHeckman.merge(SDSS, left_on='SimbadName', right_on='ident')
    data = data.drop(columns=['ident'])

    # Ensure columns are floats and removing weird symbols
    for column in ['mag_u', 'mag_g', 'mag_r', 'mag_i', 'mag_z']:
        # Replacing ~ with nan
        data[column][data[column] == '~'] = np.nan

        data[column] = data[column].astype(float)

    # Converting asinh mag to flux
    data['mag_u'] = asinh_mag_to_flux_density(data['mag_u'], 3767, 1.4*10**-10)*10**6
    data['mag_g'] = asinh_mag_to_flux_density(data['mag_g'], 3631, 0.9 * 10 ** -10) * 10 ** 6
    data['mag_r'] = asinh_mag_to_flux_density(data['mag_r'], 3631, 1.2 * 10 ** -10) * 10 ** 6
    data['mag_i'] = asinh_mag_to_flux_density(data['mag_i'], 3631, 1.8 * 10 ** -10) * 10 ** 6
    data['mag_z'] = asinh_mag_to_flux_density(data['mag_z'], 3565, 7.4 * 10 ** -10) * 10 ** 6

    # Some fluxes might be less than 0, so setting them to 0
    for column in ['mag_u', 'mag_g', 'mag_r', 'mag_i', 'mag_z']:
        data[column][data[column] < 0] = 0


    data = data.rename({'mag_u': 'flux_u', 'mag_g': 'flux_g', 'mag_r': 'flux_r', 'mag_i': 'flux_i', 'mag_z': 'flux_z'},
                       axis='columns')

    # Classifying them in my way
    data['Classification'] = data.apply(create_classification, axis=1)
    data = data.drop(columns=['A', 'M', 'L', 'H'])

    # Saving data
    data.to_csv("../../Data/Best&Heckman/BestHeckman+SDSS.csv", index=False)

    # Also saving coordinates for wise
    coord = data[['SimbadName', 'RAJ2000', 'DEJ2000']]
    coord = coord.rename({'SimbadName': 'object', 'RAJ2000': 'ra', 'DEJ2000': 'dec'}, axis='columns')

    # Currently still strings
    coord[['ra', 'dec']] = coord[['ra', 'dec']].astype(float)

    # Converting to an astropy table so it can easily be saved in ipac format
    coord = QTable.from_pandas(coord)
    ascii.write(coord, "../../Data/Best&Heckman/ra_dec.tbl", format='ipac', overwrite=True, definition='left')

