def rename_columns(df, drop=True):
    old_names = dict(well=['well', 'скваж', 'skw_nam', 'скв', 'well identifier', '№ скваж',
                           'skw', 's3', 'ed3', 'wellbore', 'скважина', '№ скваж'],
                     well_id=['skw_id'],
                     top=['top', 'верх', 'кровля'],
                     bot=['bot', 'низ', 'подош'],
                     layer=['пласт', 'plast', 'formation'],
                     layer_id=['код_пласта'],
                     level=['surface', 's6', 'ed8', 'гориз', 'goriz', 'fk_formation', 'гор', 'код горизонта'],
                     area=['ed7', 's5', 'mest', 'площадь', 'площ', 'pl'],
                     field=['s4', 'ed6', 'месторождение', 'мест', 'mest'],
                     date=['дата перфорации', 'дата', 's9', 'ed11', 'дата_перф', 'дата_ис',
                           'конец_рем', 'дата_бур', 'дата выявления старт', 'date'],
                     end=['дата выявления стоп'],
                     agent_code=['s12', 'agent', 'fk_agent_inj'],
                     agent=['агент'],
                     year=['s10', 'ed4', 'год', 'year', 'год расчета'],
                     month=['s11', 'ed5', 'month', 'месяц', 'месяц расчета'],
                     work_hours=['s15', 'ed12', 'vrabskw', 'worktime', 'время работы', 'время эксплуатации'],
                     type=['цель', 'вид_ис', 'осн_вид_работ', 'код'],
                     type_wc=['тип обводненности'],
                     reason=['причина обводнения'],
                     type_perf=['тип перфорации', 'тип'],
                     md=['md'],
                     q_oil=['добыча нефти за мес по скваж, т', 'ed14', 'ndobt', 'oil_volumetric', 'добыча нефти, м3'],
                     q_water=['добыча воды за мес по скваж, т', 'ed15', 'wdobt', 'water_volumetric', 'добыча воды, м3'],
                     q_water3=['s16', 'zakmesk', 'injection_volumetric', 'общая закачка'],
                     sgw=['ed22', 'wvespr', 'water_density', 'процент обв, вес'],
                     category=['гтм если есть'],
                     pressure=['давл'],
                     x=['x', 'coordinates_x'],
                     y=['y', 'coordinates_y'],
                     ngdu=['ed1', 's1', 'ngdu'])
    col_names = {k: '' for k in old_names.keys()}
    # search for same names
    for column in df.columns.values:
        if type(column) is not str:
            continue
        else:
            for k, v in old_names.items():
                if column in v:
                    col_names[k] = column
                    break
    df.rename(columns={v: k for k, v in col_names.items()}, inplace=True)
    col_names_set = set(df.columns)
    if drop:
        df.drop(columns=list(col_names_set.difference(col_names.keys())),
                inplace=True)

    return df


def well_renaming(w_name):
    if type(w_name) is not str:
        w_name = str(w_name)
    w_name = w_name.lower().strip().split('/')[0]
    return w_name


# метод заменяет в названиях скважин буквы с латиницы на кириллицу
# может принимать на вход массив или просто название (тогда аргумент one=True)
# пример использования: dfl2['Number'] = transliteration(dfl2['Number'])
def transliteration(numbers, one=True):
    # словарь замен
    letters = {'bgs': 'бгс', 'bg': 'бг', 'gs': 'гс', 'gc': 'гс', 'a': 'а', 'd': 'д',
               'g': 'г', 'k': 'к', 'l': 'л', 'm': 'м', 'r': 'р',
               's': 'с', 'u': 'у', 'v': 'в', 'x': 'х', 'z': 'з'}

    # применение словаря замен к названию
    def trans(number):
        if type(number) is not str:
            return number
        else:
            number = number.lower()
        for letter in letters.keys():
            number = number.replace(letter, letters[letter])
        return number

    if one:
        return trans(numbers.lower())
    else:
        for i in range(len(numbers)):
            numbers[i] = trans(numbers[i])
        return numbers


def processing_df(df, drop=True, rename=True):
    if rename:
        df.rename(columns=lambda x: x if type(
            x) is not str else x.lower().strip(), inplace=True)
        df = rename_columns(df, drop)
    if 'well' in df.columns:
        df['well'] = df['well'].apply(well_renaming)
        df['well'] = df['well'].apply(lambda x: x.split('т')[0]+'д' if x.endswith('т') else x)
    return df