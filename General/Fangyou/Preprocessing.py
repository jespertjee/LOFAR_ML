import numpy as np
from astropy.table import Table
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.linear_model import LinearRegression

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


def impute_by_regression(data, column_x, column_y):
    """
    Impute column_y by column_x using linear regression

    :param data:
    :param column_x:
    :param column_y:
    :return:
    """
    # Selecting the data
    relevant_data = data[[column_x, column_y]].dropna()

    if len(relevant_data) == 0:
        return data

    X = relevant_data[column_x]
    y = relevant_data[column_y]

    X = X.to_numpy().reshape(-1, 1)

    reg = LinearRegression().fit(X, y)

    # Filling in missing y-data
    X_for_missing_y = data[column_x][data[column_y].isna()].dropna()
    if len(X_for_missing_y) == 0:
        return data
    predicted = reg.predict(X_for_missing_y.to_numpy().reshape(-1, 1))

    predicted_df = pd.Series(predicted, index=X_for_missing_y.index)

    data[column_y] = data[column_y].fillna(predicted_df)
    return data


if __name__ == "__main__":
    pd.options.mode.chained_assignment = None
    # Opening file which has source_name to classification and some other info we might use for classification
    source_to_class = pd.read_csv("../../Data/Philip_data/Cleaned/Combined_secure_class.csv")
    source_to_class = source_to_class[["Source_Name", "AGN_final", "RadioAGN_final", "Classification",
                                       'Radio_excess', 'AGNfrac_af', 'AGNfrac_af_16', 'AGNfrac_cg_s_16',
                                       'Xray', 'Opt_spec', 'IRAGN', 'Extended_radio']]

    # Opening raw data and matching it to source
    filled_data = []
    non_filled_data = []

    file_locations = [
        '../../Data/Fangyou_data/Original/Radio/Cross_match/bootes_final_cross_match_catalogue-v0.8.fits',
        '../../Data/Fangyou_data/Original/Radio/Cross_match/en1_final_cross_match_catalogue-v0.8.fits',
        '../../Data/Fangyou_data/Original/Radio/Cross_match/lockman_final_cross_match_catalogue-v0.8.fits']
    save_locations = [
        '../../Data/Fangyou_data/Cleaned/Bootes_preprocessed.csv',
        '../../Data/Fangyou_data/Cleaned/Elais-N1_preprocessed.csv',
        '../../Data/Fangyou_data/Cleaned/Lockman_preprocessed.csv'
    ]

    for i, file, save_location in zip([0,1,2], file_locations, save_locations):
        # Opening file
        dat = open_fits(file)

        # Columns to remove, namely the errors and the magnitudes (mag are simply conversions from flux,
        # so not interesting
        remove_columns_error = [column for column in dat.columns if 'err' in column.lower()]
        #dat = dat.drop(columns=remove_columns_error)
        remove_columns_mag = [column for column in dat.columns if 'mag' in column.lower()]
        dat = dat.drop(columns=remove_columns_mag)

        # Drop generic columns
        remove_columns_generic = ["E_RA", "E_DEC", "E_Maj", "E_Min", "E_PA", "Maj", "Min",
                                  "PA", "DC_Maj", "DC_Min", "DC_PA", "Isl_rms", "FLAG_WORKFLOW", "Prefilter",
                                  "NoID", "lr_fin", "optRA", "optDec", "LGZ_Size", "LGZ_Width", "LGZ_PA", "Assoc",
                                  "Assoc_Qual", "Art_prob", "Blend_prob", "Hostbroken_prob", "Zoom_prob",
                                  "Created", "Position_from", "Renamed_from", "FLAG_OVERLAP_RADIO", "flag_clean_radio",
                                  "ALPHA_J2000", "DELTA_J2000", "flag_clean", "ID_OPTICAL", "ID_SPITZER",
                                  "ID", "FLAG_OVERLAP", "Separation", "help_id", "RA_HELP", "DEC_HELP", "CLASS_STAR",
                                  "flag_mips_24", "Pval_res_24", "Bkg_MIPS_24", "Sig_conf_MIPS_24", "Rhat_MIPS_24",
                                  "n_eff_MIPS_24", "Pval_res_24", "flag_mips_24", "Bkg_PACS_100", "Bkg_PACS_160",
                                  "Sig_conf_PACS_100", "Sig_conf_PACS_160", "Rhat_PACS_100", "Rhat_PACS_160",
                                  "n_eff_PACS_100", "n_eff_PACS_160", "Pval_res_100", "Pval_res_160", "flag_PACS_100",
                                  "flag_PACS_160", "Bkg_SPIRE_250", "Bkg_SPIRE_350", "Bkg_SPIRE_500",
                                  "Sig_conf_SPIRE_250", "Sig_conf_SPIRE_350", "Sig_conf_SPIRE_500", "Rhat_SPIRE_250",
                                  "Rhat_SPIRE_350", "Rhat_SPIRE_500", "n_eff_SPIRE_250", "n_eff_SPIRE_500",
                                  "n_eff_SPIRE_350", "Pval_res_250", "Pval_res_350", "Pval_res_500", "flag_spire_250",
                                  "flag_spire_350", "flag_spire_500", "Z_BEST_SOURCE", "Z_SPEC",
                                  "z1_median", "z1_min", "z1_max", "z1_area", 
                                  "z2_median", "z2_min", "z2_max", "z2_area", "nfilt_eazy", "nfilt_atlas",
                                  "nfilt_ananna", "chi_r_best", "chi_r_stellar", "stellar_type", "AGN", "optAGN",
                                  "IRAGN", "XrayAGN",
                                  "ap_to_model_z", "zmodel", "chi_best", "Nfilts",
                                  "u_rest", "z_rest",
                                  "J_rest", "K_rest",
                                  "XID+_rerun_mips", "XID+_rerun_pacs", "XID+_rerun_SPIRE"]
        dat = dat.drop(columns=remove_columns_generic)

        # Converting units to microJanskies
        dat[["Total_flux", "Peak_flux"]] = dat[["Total_flux", "Peak_flux"]]*10**6
        dat[["F_PACS_100", "F_PACS_160", "F_SPIRE_250", "F_SPIRE_350", "F_SPIRE_500"]] = \
            dat[["F_PACS_100", "F_PACS_160", "F_SPIRE_250", "F_SPIRE_350", "F_SPIRE_500"]]*10**3

        # Drop table-specific columns
        if i==0:
            dat = dat.drop(columns=['FLAG_DEEP', 'RA_ZSPEC', 'DEC_ZSPEC', 'REL', 'OBJID', 'AGN_ZSPEC', 'XrayFlux_0.5-2',
                                    'XrayHardness', 'ap_to_model_z_Subaru', 'Bw_rest', 'R_rest', 'I_rest',
                                    'z_Subaru_rest', 'H_rest', 'Ks_rest', 'ch1_rest', 'ch2_rest', 'ch3_rest',
                                    'ch4_rest', 'Z_SOURCE', 'Z_QUAL', 'y_rest'])
            dat["Source"] = 'Bootes'
        if i==1:
            dat = dat.drop(columns=['Z_SOURCE', 'Z_QUAL', 'y_rest', '2RXS_ID', 'XMMSL2_ID',
                                    'ap_to_model_g', 'ap_to_model_r', 'g_rest', 'r_rest', 'i_rest', 'ch1_servs_rest',
                                    'ch2_servs_rest', 'ch1_swire_rest', 'ch2_swire_rest', 'ch3_swire_rest',
                                    'ch4_swire_rest'])
            dat["Source"] = 'Elais-N1'
        if i==2:
            dat = dat.drop(columns=['2RXS_ID', 'XMMSL2_ID', 'ap_to_model_g', 'ap_to_model_r', 'g_rest',
                                    'g_rest', 'g_rcs_rest', 'r_rcs_rest', 'i_rcs_rest', 'z_rcs_rest', 'ch1_servs_rest',
                                    'ch2_servs_rest', 'ch1_swire_rest', 'ch2_swire_rest', 'ch3_swire_rest',
                                    'ch4_swire_rest', 'r_rest'])
            dat["Source"] = 'Lockman'

        # Changing column to strings instead of bytes
        dat['S_Code'] = dat['S_Code'].apply(lambda s: s.decode('utf-8'))

        # MIPS/PACS/SPIRE sets nan's to 1e20, so lets change that to nans
        dat["F_MIPS_24"][dat["F_MIPS_24"] > 1e10] = np.nan
        dat["F_PACS_100"][dat["F_PACS_100"] > 1e10] = np.nan
        dat["F_PACS_160"][dat["F_PACS_160"] > 1e10] = np.nan
        dat["F_SPIRE_250"][dat["F_SPIRE_250"] > 1e10] = np.nan
        dat["F_SPIRE_350"][dat["F_SPIRE_350"] > 1e10] = np.nan
        dat["F_SPIRE_500"][dat["F_SPIRE_500"] > 1e10] = np.nan

        # Similar thing for the errors
        dat["FErr_MIPS_24_u"][dat["FErr_MIPS_24_u"] > 1e10] = np.nan
        dat["FErr_MIPS_24_l"][dat["FErr_MIPS_24_l"] > 1e10] = np.nan
        dat["FErr_PACS_100_u"][dat["FErr_PACS_100_u"] > 1e10] = np.nan
        dat["FErr_PACS_100_l"][dat["FErr_PACS_100_l"] > 1e10] = np.nan
        dat["FErr_PACS_160_u"][dat["FErr_PACS_160_u"] > 1e10] = np.nan
        dat["FErr_PACS_160_l"][dat["FErr_PACS_160_l"] > 1e10] = np.nan
        dat["FErr_SPIRE_250_u"][dat["FErr_SPIRE_250_u"] > 1e10] = np.nan
        dat["FErr_SPIRE_250_l"][dat["FErr_SPIRE_250_l"] > 1e10] = np.nan
        dat["FErr_SPIRE_350_u"][dat["FErr_SPIRE_350_u"] > 1e10] = np.nan
        dat["FErr_SPIRE_350_l"][dat["FErr_SPIRE_350_l"] > 1e10] = np.nan
        dat["FErr_SPIRE_500_u"][dat["FErr_SPIRE_500_u"] > 1e10] = np.nan
        dat["FErr_SPIRE_500_l"][dat["FErr_SPIRE_500_l"] > 1e10] = np.nan

        print(len(dat[dat["F_SPIRE_500"] > 1e10]["F_SPIRE_500"]))

        # Setting negative values to nan (later they should be set to the minimum
        dat_num = dat.select_dtypes(include=[float])
        dat[dat_num<0] = np.nan

        # Fixing the source name column, since it is currently saved in bytes and should become a string
        dat['Source_Name'] = dat['Source_Name'].apply(lambda s: s.decode('utf-8'))
        dat = dat.merge(source_to_class, on='Source_Name')

        # Data where minima haven't been filled yet
        non_filled_data.append(dat.copy())

        filled_data.append(dat.copy())

    # Data that won't be filled
    combined_non_filled = pd.concat(non_filled_data, ignore_index=True)
    combined_non_filled.to_csv('../../Data/Fangyou_data/Cleaned/combined_non_filled_preprocessed.csv', index=False)

    # Data that will be filled First we fill the missing values,
    # the first strategy to use is see if there is a similar filter which we can use to get the data
    for i, dat in enumerate(non_filled_data):
        if i == 0:
            # Filling columns by each other
            dat["z_flux_corr"] = dat["z_flux_corr"].fillna(dat["z_Subaru_flux_corr"])
            dat["z_Subaru_flux_corr"] = dat["z_Subaru_flux_corr"].fillna(dat["z_flux_corr"])
            dat["z_rcs_flux_corr"] = dat["z_flux_corr"]
            dat["z_hsc_flux_corr"] = dat["z_flux_corr"]

            dat["i_hsc_flux_corr"] = dat["I_flux_corr"]
            dat["i_rcs_flux_corr"] = dat["I_flux_corr"]
            dat["i_flux_corr"] = dat["I_flux_corr"]

            dat["y_hsc_flux_corr"] = dat["y_flux_corr"]

            dat["r_flux_corr"] = dat["R_flux_corr"]
            dat["r_hsc_flux_corr"] = dat["R_flux_corr"]
            dat["r_rcs_flux_corr"] = dat["R_flux_corr"]

            dat["ch1_swire_flux_corr"] = dat["ch1_flux_corr"]
            dat["ch2_swire_flux_corr"] = dat["ch2_flux_corr"]
            dat["ch3_swire_flux_corr"] = dat["ch3_flux_corr"]
            dat["ch4_swire_flux_corr"] = dat["ch4_flux_corr"]

            dat["ch1_servs_flux_corr"] = dat["ch1_flux_corr"]
            dat["ch2_servs_flux_corr"] = dat["ch2_flux_corr"]
        if i == 1:
            dat["z_Subaru_flux_corr"] = dat["z_flux_corr"]
            dat["z_rcs_flux_corr"] = dat["z_flux_corr"]

            dat["i_rcs_flux_corr"] = dat["i_flux_corr"]
            dat["I_flux_corr"] = dat["i_flux_corr"]

            dat["g_rcs_flux_corr"] = dat["g_hsc_flux_corr"]

            dat["R_flux_corr"] = dat["r_flux_corr"]
            dat["r_rcs_flux_corr"] = dat["r_flux_corr"]

            dat["ch1_flux_corr"] = dat["ch1_swire_flux_corr"]
            dat["ch2_flux_corr"] = dat["ch2_swire_flux_corr"]
            dat["ch3_flux_corr"] = dat["ch3_swire_flux_corr"]
            dat["ch4_flux_corr"] = dat["ch4_swire_flux_corr"]
        if i == 2:
            dat["z_Subaru_flux_corr"] = dat["z_flux_corr"]
            dat["z_hsc_flux_corr"] = dat["z_flux_corr"]

            dat["R_flux_corr"] = dat["r_flux_corr"]
            dat["r_hsc_flux_corr"] = dat["r_flux_corr"]

            dat["I_flux_corr"] = dat["i_rcs_flux_corr"]
            dat["i_hsc_flux_corr"] = dat["i_rcs_flux_corr"]
            dat["i_flux_corr"] = dat["i_rcs_flux_corr"]

            dat["g_hsc_flux_corr"] = dat["g_flux_corr"]

            dat["ch1_flux_corr"] = dat["ch1_swire_flux_corr"]
            dat["ch2_flux_corr"] = dat["ch2_swire_flux_corr"]
            dat["ch3_flux_corr"] = dat["ch3_swire_flux_corr"]
            dat["ch4_flux_corr"] = dat["ch4_swire_flux_corr"]

        filled_data[i] = dat

    combined_filled = pd.concat(filled_data, ignore_index=True)

    combined_filled.to_csv('../../Data/Fangyou_data/Cleaned/combined_using_similar_columns.csv', index=False)

    # Using a correlation matrix to impute missing values
    corr = combined_filled.drop(columns=["Source_Name", "S_Code",
                       "EBV", "AGN_final", "RadioAGN_final",
                       "Classification", "Radio_excess", "AGNfrac_af",
                       "AGNfrac_af_16", "AGNfrac_cg_s_16", "Source"]).corr()
    for column in combined_filled.columns:
        if column not in ["Source_Name", "Total_flux", "Peak_flux", "S_Code", "EBV", "Z_BEST", "Mass_median",
                          "Mass_l68", "Mass_u68", "AGN_final", "RadioAGN_final", "Classification", "Radio_excess",
                          "AGNfrac_af", "AGNfrac_af_16", "AGNfrac_cg_s_16", "Source"]:
            print(f"Imputing {column}")

            sorted_corr = corr[column].sort_values(ascending=False)
            # Only selecting correlations above 0.7
            sorted_corr = sorted_corr[sorted_corr>0.7]
            for x_column in sorted_corr.index:
                # Not selecting itself of course, since that always has a correlation of 1
                if x_column != column:
                    combined_filled = impute_by_regression(combined_filled, x_column, column)

    # Lastly the final missing values will simply be imputed with the minimum
    for column in ["FUV_flux_corr", "NUV_flux_corr", "u_flux_corr", "Bw_flux_corr", "R_flux_corr", "I_flux_corr",
                   "z_flux_corr", "z_Subaru_flux_corr", "F_MIPS_24", "F_PACS_100", "F_PACS_160", "F_SPIRE_250",
                   "F_SPIRE_350", "F_SPIRE_500", "Mass_median", "Mass_l68", "Mass_u68"]:
        minimum = np.nanmin(combined_filled[column])
        combined_filled[column] = combined_filled[column].fillna(minimum)

    # Setting any negative values to 0
    numeric_columns = list(combined_filled.select_dtypes(include=[np.number]).columns.values)
    combined_filled[numeric_columns][combined_filled[numeric_columns]<0] = 0


    print(combined_filled.isna().sum())

    combined_filled.to_csv('../../Data/Fangyou_data/Cleaned/combined_filled_with_regression.csv', index=False)



