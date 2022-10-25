import pandas as pd

from rest.readers.read_service import processing_df


def read_coords(file):
    coords_df = pd.read_csv(file)
    coords_df = processing_df(coords_df)
    coords_df.dropna(inplace=True)
    coords_dict = coords_df.to_dict(orient='records')

    return coords_dict
