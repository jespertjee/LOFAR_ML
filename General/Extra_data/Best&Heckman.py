import pandas as pd
from Get_SDSS_names import open_fits
import numpy as np

if __name__ == "__main__":
    BestHeckman = open_fits("../../Data/Best&Heckman/Best&Heckman2012.fit")
    SDSS = pd.read_csv("../../Data/Best&Heckman/SDSS.csv")

    # Fixing the source name column, since it is currently saved in bytes and should become a string
    BestHeckman['SimbadName'] = BestHeckman['SimbadName'].apply(lambda s: s.decode('utf-8')).str[0:-1]

    data = BestHeckman.merge(SDSS, left_on='SimbadName', right_on='ident')
    data = data.drop(columns=['ident'])

    # Converting AB mag to mJy
    for column in ['mag_u', 'mag_g', 'mag_r', 'mag_i', 'mag_z']:
        # Replacing ~ with nan
        data[column][data[column] == '~'] = np.nan

        data[column] = data[column].astype(float)
        data[column] = 3631 * 10**6 * 10**(-data[column]/2.5)

    data = data.rename({'mag_u': 'flux_u', 'mag_g': 'flux_g', 'mag_r': 'flux_r', 'mag_i': 'flux_i', 'mag_z': 'flux_z'},
                       axis='columns')

    # Saving data
    data.to_csv("../../Data/Best&Heckman/BestHeckman+SDSS.csv", index=False)