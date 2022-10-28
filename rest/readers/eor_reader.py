import logging
import sys

import numpy as np
from dateutil import parser

from rest.readers.read_service import read_df, processing_df
from rest.util import to_dict


def read(file):
    eor_df = read_df(file)
    eor_df = processing_df(eor_df)
    eor_df['date'] = eor_df['date'].apply(lambda str_date: parser.parse(str_date).date())

    if 'year' not in eor_df.columns:
        eor_df['year'] = eor_df['date'].apply(lambda x: x.year)
        eor_df['month'] = eor_df['date'].apply(lambda x: x.month)
    eor_df.reset_index(drop=True, inplace=True)
    for col in ['q_water3', 'work_hours']:
        if col in eor_df.columns:
            eor_df[col] = eor_df[col].apply(lambda x: x.replace(',', '.') if type(x) == str else x)
            eor_df[col] = eor_df[col].astype(float)

    return eor_df


def read_eor_inj(file):
    eor_df = read(file)
    if 'agent_code' not in eor_df.columns and 'agent' in eor_df.columns:
        eor_df['agent_code'] = eor_df['agent'].apply(get_agent_code)

    columns = ['well', 'year', 'month', 'date', 'work_hours', 'q_water3', 'agent_code', 'level', 'layer']
    drop_cols = [col for col in eor_df.columns if col not in columns]
    eor_df.drop(columns=drop_cols,
                inplace=True)

    eor_df = eor_df.sort_values(by=['well', 'year'])
    eor_df.reset_index(drop=True, inplace=True)
    eor_df['acceleration'] = (eor_df['q_water3'] * 24) / eor_df['work_hours']
    eor_df['acceleration'] = eor_df['acceleration'].fillna(0)

    eor_df.reset_index(drop=True, inplace=True)
    eor = to_dict(eor_df, 'well')

    return eor


def read_eor_prod(file, unit='t'):
    eor_df = read(file)
    columns = ['well', 'year', 'month', 'date', 'work_hours', 'q_oil', 'q_water', 'sgw', 'level', 'layer']
    drop_cols = [col for col in eor_df.columns if col not in columns]
    eor_df.drop(columns=drop_cols,
                inplace=True)

    eor_df = eor_df.sort_values(by=['well', 'year'])
    eor_df.reset_index(drop=True, inplace=True)
    if 'sgw' in eor_df.columns:
        eor_df['sgw'] = eor_df['sgw'].replace(np.NaN, 1.1)
    if unit == 't':
        if 'sgw' not in eor_df.columns:
            logging.error("Нет данных по процентному весу обводнения")
            sys.exit()
        p_water = eor_df['q_water'] / eor_df['sgw']
        p_water.fillna(0, inplace=True)
        eor_df['fluid_rate'] = ((p_water + eor_df['q_oil'] * 1.34) * 24) / eor_df['work_hours']
    else:
        eor_df['fluid_rate'] = ((eor_df['q_water'] + eor_df['q_oil']) * 24) / eor_df['work_hours']

    eor_df.reset_index(drop=True, inplace=True)
    eor = to_dict(eor_df, 'well')
    return eor


def get_agent_code(agent):
    if 'пресн' in agent:
        return 1
    elif 'сточн' in agent:
        return 2
    elif 'пласт' in agent:
        return 3
    else:
        return -1
