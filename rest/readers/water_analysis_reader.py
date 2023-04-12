from dateutil import parser

from rest.readers.read_service import read_df, processing_df
from rest.util import to_dict


def read_water_analysis(file):
    water_analysis_df = read_df(file)
    water_analysis_df = processing_df(water_analysis_df)
    columns = ['well', 'date', 'mineralization', 'level', 'sulfate', 'field']
    drop_cols = [col for col in water_analysis_df.columns if col not in columns]
    water_analysis_df.drop(columns=drop_cols,
                           inplace=True)
    water_analysis_df['date'] = water_analysis_df['date'].apply(lambda str_date: parser.parse(str_date).date())

    water_analysis = to_dict(water_analysis_df, 'well')
    return water_analysis
