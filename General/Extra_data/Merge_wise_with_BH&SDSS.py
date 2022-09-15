from astropy.io import ascii
import pandas as pd

if __name__ == "__main__":
    data_wise = ascii.read("../../Data/Best&Heckman/wise.txt").to_pandas()

    # Dropping uninteresting data
    # TODO: drop errors as well here, they aren't of any use
    data_wise = data_wise.drop(columns=['cntr_01', 'dist_x', 'pang_x', 'ra_01', 'dec_01', 'designation', 'sigra', 'sigdec',
                              'sigradec', 'w1snr', 'w1rchi2', 'w2snr', 'w2rchi2',
                              'w3snr', 'w3rchi2', 'w4snr', 'w4rchi2', 'nb', 'na', 'w1sat', 'w2sat',
                              'w3sat', 'w4sat', 'cc_flags', 'ext_flg', 'var_flg', 'moon_lev', 'w1nm', 'w1m', 'w2nm',
                              'w2m', 'w3nm', 'w3m', 'w4nm', 'w4m', 'j_msig_2mass', 'h_msig_2mass', 'k_msig_2mass'])


    # Renaming the wise ra and dec
    data_wise = data_wise.rename({'ra': 'wise_ra', 'dec': 'wise_dec'}, axis='columns')

    # Renaming other columns to that they make more sense
    data_wise = data_wise.rename({'object_01': 'SimbadName', 'w1mpro': 'w1_wise', 'w2mpro': 'w2_wise', 'w3mpro': 'w3_wise',
                        'w4mpro': 'w4_wise', 'w1sigmpro': 'w1mag_wise_error', 'w2sigmpro': 'w2mag_wise_error',
                        'w3sigmpro': 'w3mag_wise_error', 'w4sigmpro': 'w4mag_wise_error', 'j_m_2mass': 'j_2mass',
                        'h_m_2mass': 'h_2mass', 'k_m_2mass': 'k_2mass'}, axis='columns')

    # Converting magnitudes to fluxes
    # Using https://wise2.ipac.caltech.edu/docs/release/allsky/expsup/sec4_4h.html for wise
    # Converting to uJy
    data_wise['w1_wise'] = 309.540 * 10 ** (-data_wise['w1_wise']/2.5) *10**6
    data_wise['w2_wise'] = 171.787 * 10 ** (-data_wise['w2_wise'] / 2.5)*10**6
    data_wise['w3_wise'] = 31.674  * 10 ** (-data_wise['w3_wise'] / 2.5)*10**6
    data_wise['w4_wise'] = 8.363   * 10 ** (-data_wise['w4_wise'] / 2.5)*10**6

    data_wise['j_2mass'] = 1594  * 10 ** (-data_wise['j_2mass'] / 2.5) * 10 ** 6
    data_wise['h_2mass'] = 1024  * 10 ** (-data_wise['h_2mass'] / 2.5) * 10 ** 6
    data_wise['k_2mass'] = 666.7  * 10 ** (-data_wise['k_2mass'] / 2.5) * 10 ** 6

    data_wise.to_csv("../../Data/Best&Heckman/wise.csv", index=False)

    # Now cross-matching that to the SDDS and B&H data
    SDDS_BH_data = pd.read_csv("../../Data/Best&Heckman/BestHeckman+SDSS.csv")

    SDDS_BH_data = SDDS_BH_data.merge(data_wise, on='SimbadName')

    SDDS_BH_data.to_csv('../../Data/Best&Heckman/BestHeckman+SDSS+wise.csv', index=False)


