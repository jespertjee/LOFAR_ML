import pandas as pd
from os import listdir

# We need to ignore already downloaded files
file_names = [f[0:-5] for f in listdir("./downloaded_data")]

data_name = '../../../Data/Fangyou_data/Cleaned/combined_non_filled_preprocessed.csv'

# Only selecting columns we are interested in
data = pd.read_csv(data_name)[["Source_Name", "RA", "DEC", 'Source']]

# Only selecting Elais-N1
data = data[data['Source'] == 'Elais-N1']
data = data.drop(columns='Source')

# Ignoring already download files
data = data[~data['Source_Name'].isin(file_names)]

# Settings
rerun = 'pdr3_dud'
filt = 'HSC-I'
sw = sh = '5asec'
image_bool = 'true'
mask_bool = 'true'
variance_bool = 'true'

# Filling in the settings
data['rerun'] = rerun
data['ra'] = data['RA']
data['dec'] = data['DEC']
data = data.drop(columns=['RA', 'DEC'])
data['sw'] = sw
data['sh'] = sh
data['filter'] = filt
data['image'] = image_bool
data['mask'] = mask_bool
data['variance'] = variance_bool
data['name'] = data['Source_Name']
data = data.drop(columns='Source_Name')

data.to_csv('test.txt', index=False, sep=' ', )
