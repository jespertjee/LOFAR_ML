import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.linear_model import LinearRegression

"""
Purpose of this file is to postpreprocess the classification.txt file, 
mostly to convert units
"""

if __name__ == "__main__":
    for file in ['', '_secure']:
        data = pd.read_csv(f'../../Data/MIGHTEE/Classification/combined{file}.csv')

        # Setting negative fluxes to nan
        fluxes = ['S_INT14', 'S_PEAK14', 'ch1_flux_corr',
           'ch2_flux_corr', 'ch3_flux_corr', 'ch4_flux_corr', 'F_MIPS_24',
           'F_PACS_100', 'F_PACS_160', 'F_SPIRE_250', 'F_SPIRE_350', 'F_SPIRE_500',
           'EBV', 'Ks_flux_corr', 'H_flux_corr', 'J_flux_corr', 'i_flux_corr',
           'r_flux_corr', 'u_flux_corr', 'z_flux_corr', 'y_flux_corr',
           'NUV_flux_corr', 'FUV_flux_corr']
        data[data[fluxes] < 0] = np.nan

        # Converting fluxes from mJy to uJy
        data[['ch1_flux_corr',
           'ch2_flux_corr', 'ch3_flux_corr', 'ch4_flux_corr', 'F_MIPS_24',
           'F_PACS_100', 'F_PACS_160', 'F_SPIRE_250', 'F_SPIRE_350', 'F_SPIRE_500']] *= 1000


        data.to_csv(f"../../Data/MIGHTEE/Classification/Combined{file}_postprocessed.csv", index=False)