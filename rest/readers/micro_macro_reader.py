from rest.readers.read_service import read_df, processing_df
from dateutil import parser


components = ['li', 'be', 'b', 'na', 'mg', 'al', 'k',
              'ca', 'sc', 'ti', 'v', 'cr', 'mn', 'fe', 'co', 'ni', 'cu', 'zn', 'ga',
              'ge', 'as', 'se', 'rb', 'sr', 'y', 'zr', 'nb', 'mo', 'ru', 'rh', 'ag',
              'pd', 'cd', 'sn', 'sb', 'te', 'cs', 'ba', 'la', 'ce', 'pr', 'nd', 'sm',
              'eu', 'gd', 'tb', 'dy', 'ho', 'er', 'tm', 'yb', 'lu', 'hf', 'ta', 'w',
              're', 'os', 'ir', 'pt', 'au', 'tl', 'pb', 'bi', 'th', 'u']

fields = ['well', 'ngdu', 'field', 'date', 'area', 'comment', 'layer']


def read_micro_macro(file, headers=None):
    df = read_df(file)
    df = processing_df(df, drop=False, headers=headers)
    df.drop(columns=list(set(df.columns).difference(fields + components)),
            inplace=True)

    device = df.loc[0, 'li']
    device_val = df.drop(columns=list(set(df.columns).intersection(fields + ['device']))).loc[1].to_dict()
    df.drop([0, 1], inplace=True)
    df.replace('<ПО', 0, inplace=True)
    df['device'] = device
    df.dropna(subset=['well', 'date', 'ngdu'], inplace=True)

    if 'layer' in df.columns:
        df['layer'] = df['layer'].str.replace(' ', '').str.replace('\n', ',').fillna(method='ffill')

    try:
        df['date'] = df['date'].dt.date
    except AttributeError:
        df['date'] = df['date'].apply(
            lambda str_date: parser.parse(str_date).date())

    micro_macro = df[list(set(df.columns).intersection(fields + ['device']))].to_dict(orient='records')
    components_dict_jar = df[list(set(df.columns).intersection(components))].to_dict(orient='records')

    components_dict = []
    for comp in components_dict_jar:
        components_dict.append({k: dict(value=v, device_val=device_val[k]) for k, v in comp.items()})

    return micro_macro, components_dict
