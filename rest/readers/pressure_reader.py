import pandas as pd
from dateutil import parser

from rest.readers.read_service import read_df, processing_df
from rest.util import to_dict


def read_pressure(file):
    hds_df = read_df(file)
    hds_df = processing_df(hds_df)
    hds_df['type'] = hds_df['type'].str.strip().str.lower()
    try:
        hds_df['date'] = hds_df['date'].dt.date
    except AttributeError:
        hds_df['date'] = hds_df['date'].apply(
            lambda str_date: parser.parse(str_date).date())
    hds_df['date'] = pd.to_datetime(hds_df['date'])
    hds_df['type'].replace(to_replace={'p заб': 'н дин', 'p пл': 'н ст'}, inplace=True)
    columns = ['well', 'pressure', 'date', 'type', 'level', 'mark', 'productivity', 'q_fluid']
    drop_cols = [col for col in hds_df.columns if col not in columns]
    hds_df.drop(columns=drop_cols,
                inplace=True)
    hds = to_dict(hds_df, 'well')
    return hds
