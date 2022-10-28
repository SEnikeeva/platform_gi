from dateutil import parser

from rest.readers.read_service import read_df, processing_df


def read_mineralization(file):

    salinity_df = read_df(file, sep=';', enc='cp1251')
    salinity_df = processing_df(salinity_df, rename=False)
    salinity_df.dropna(inplace=True)
    salinity_df['start'] = salinity_df['start'].apply(
                lambda str_date: parser.parse(str_date, dayfirst=True).date())
    salinity_df['end'] = salinity_df['end'].apply(
        lambda str_date: parser.parse(str_date, dayfirst=True).date())
    salinity = salinity_df.to_dict(orient='records')
    return salinity
