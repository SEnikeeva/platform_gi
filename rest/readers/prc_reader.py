from rest.readers.read_service import read_df, processing_df
from rest.util import to_dict


def read_prc(file):
    prc_df = read_df(file)
    prc_df = processing_df(prc_df)
    columns = ['well', 'date', 'productivity', 'level']
    drop_cols = [col for col in prc_df.columns if col not in columns]
    prc_df.drop(columns=drop_cols,
                inplace=True)
    prc = to_dict(prc_df, 'well')
    return prc
