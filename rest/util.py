from rest.models import Well, OilDeposit


def to_dict(df, index_name, columns=None):
    df.set_index(index_name, inplace=True)
    # перестановка столбцов для сохранения установленного порядка
    if columns is not None:
        df = df.reindex(columns, axis=1)
    else:
        columns = df.columns
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


def get_well_id(well_name, oil_deposit_id=None):
    well = Well.objects.filter(name=well_name, oil_deposit_id=oil_deposit_id).all()
    if len(well) == 0:
        new_well = Well.objects.create(
            oil_deposit_id=oil_deposit_id,
            name=well_name,
        )
        well_id = new_well.id
    else:
        well_id = well[0].id
    return well_id


def get_oil_deposit_id(oil_deposit_name, company_id=None):
    oil_deposit = OilDeposit.objects.filter(name=oil_deposit_name, company_id=company_id).all()
    if len(oil_deposit) == 0:
        new_oil_deposit = OilDeposit.objects.create(
            name=oil_deposit_name,
            company_id=company_id,
        )
        oil_deposit_id = new_oil_deposit.id
    else:
        oil_deposit_id = oil_deposit[0].id
    return oil_deposit_id
