import pandas as pd
from dateutil import parser

from rest.readers.read_service import read_df, processing_df
from rest.util import to_dict


def read_works(file):
    works_df = read_df(file)
    works_df = processing_df(works_df)
    works_df['type'] = works_df['type'].str.strip().str.lower()
    works_df['name'] = works_df['name'].str.strip().str.lower()
    works_df.rename({'start': 'start_date', 'end': 'end_date'}, axis=1, inplace=True)
    columns = ['well', 'start_date', 'end_date', 'type', 'name']
    drop_cols = [col for col in works_df.columns if col not in columns]
    works_df.drop(columns=drop_cols,
                  inplace=True)
    works = to_dict(works_df, 'well')
    return works
