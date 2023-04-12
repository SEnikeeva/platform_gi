from rest.readers.read_service import read_df, processing_df
from dateutil import parser


def read_six_components(file, headers=None):
    fields = ['well', 'field', 'ngdu', 'date', 'unit',
              'mineralization', 'rigidity']

    anions = ['hco3-', 'so42-', 'cl-']
    cations = ['ca2+', 'mg2+', 'na+k+']

    df = read_df(file)
    df.fillna(method='ffill', inplace=True)
    df = processing_df(df, drop=False, headers=headers)

    df.drop(columns=list(set(df.columns).difference(fields + anions + cations)),
            inplace=True)
    try:
        df['date'] = df['date'].dt.date
    except AttributeError:
        df['date'] = df['date'].apply(
            lambda str_date: parser.parse(str_date).date())

    six_components = df[list(set(df.columns).intersection(fields))].to_dict(orient='records')
    anions_dict = df[list(set(df.columns).intersection(anions))].to_dict(orient='records')
    cations_dict = df[list(set(df.columns).intersection(cations))].to_dict(orient='records')

    return six_components, anions_dict, cations_dict
