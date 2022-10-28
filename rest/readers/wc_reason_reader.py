from dateutil import parser

from rest.readers.read_service import processing_df, read_df
import chardet


def read_wc_reason(file):
    wc_reason_df = read_df(file)
    wc_reason_df = processing_df(wc_reason_df, rename=False)
    wc_reason_df['date'] = wc_reason_df['date'].apply(lambda str_date: parser.parse(str_date).date())

    wc_reason = wc_reason_df.to_dict(orient='records')
    return wc_reason
