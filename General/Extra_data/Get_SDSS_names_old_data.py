import pandas as pd

if __name__ == "__main__":
    data = pd.read_csv("../../Data/Fangyou_data/Cleaned/combined_non_filled_preprocessed.csv")

    coords = data[['RA', 'DEC']]
    coords['Coord'] = coords['RA'].astype(str) + ' ' + coords['DEC'].astype(str)
    coords = coords['Coord']

    coords.to_csv("../../Data/Best&Heckman/old_data_coords.txt", sep='\n', index=False)