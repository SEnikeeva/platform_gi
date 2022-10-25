def to_dict(df, columns, index_name):
    df.set_index(index_name, inplace=True)
    # перестановка столбцов для сохранения установленного порядка
    df = df.reindex(columns, axis=1)
    # преобразование DataFrame в словарь
    df_dict = df.groupby(level=0, sort=False) \
        .apply(lambda x: [dict(zip(columns, e))
                          for e in x.values]) \
        .to_dict()
    return df_dict


def is_contains(w, a):
    for v in a:
        if v in w:
            return True
    return False
