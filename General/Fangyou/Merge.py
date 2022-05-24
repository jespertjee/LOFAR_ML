import pandas as pd

if __name__ == "__main__":
    Bootes_data = pd.read_csv("../../Data/Fangyou_data/Cleaned/Bootes_clean.csv")
    Lockman_data = pd.read_csv("../../Data/Fangyou_data/Cleaned/Lockman_clean.csv")
    Elais_data = pd.read_csv("../../Data/Fangyou_data/Cleaned/Elais-N1_clean.csv")

    combined = pd.concat([Bootes_data, Lockman_data, Elais_data])

    combined.to_csv("../../Data/Fangyou_data/Cleaned/Combined.csv", index=False)