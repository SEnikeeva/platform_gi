from dateutil import parser

from rest.readers.read_service import read_df, processing_df


def read_mineralization(file):
    salinity_df = read_df(file, sep=';', enc='cp1251')
    salinity_df = processing_df(salinity_df, headers=None)
    salinity_df.dropna(inplace=True)
    salinity_df['start_date'] = salinity_df['start'].apply(
        lambda str_date: parser.parse(str_date, dayfirst=True).date())
    salinity_df['end_date'] = salinity_df['end'].apply(
        lambda str_date: parser.parse(str_date, dayfirst=True).date())
    columns = ['start_date', 'end_date', 'well', 'type', 'field']
    drop_cols = [col for col in salinity_df.columns if col not in columns]
    salinity_df.drop(columns=drop_cols,
                     inplace=True)
    salinity = salinity_df.to_dict(orient='records')
    return salinity
