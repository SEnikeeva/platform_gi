from dateutil import parser

from rest.readers.read_service import read_df, processing_df


def read_isotopy(file, headers=None):
    isotopy_df = read_df(file)
    isotopy_df = processing_df(isotopy_df, headers=headers)
    isotopy_df['date'] = isotopy_df['date'].apply(
        lambda str_date: parser.parse(str_date, dayfirst=True).date())
    isotopy = isotopy_df.to_dict(orient='records')
    return isotopy
