import pandas as pd
import os


def get_last_csv(category):
    '''
    Dada una category (str) devuelve el último archivo descargado
    '''
    archivos = []
    for root, dirs, files in os.walk(category):
        for name in files:
            archivo = os.path.join(root, name)
            archivos.append(archivo)
    return archivos[-1]


def normalize_headers(header):
    header = header.lower()
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        header = header.replace(a, b)
    return header


def read_csv_normalize(category: str) -> pd.DataFrame():
    file = get_last_csv(category)
    df = pd.read_csv(file)
    df.columns = [normalize_headers(column) for column in df.columns]
    return df


def df_category(category: str) -> pd.DataFrame():
    '''
    Normaliza el csv de la category y devuelve un dataframe con
    las columnas que
    interesan. Agrega una columna según la categoría
    '''
    df = read_csv_normalize(category)
    df.rename(columns={
                       'cod_loc': 'cod_localidad',
                       'idprovincia': 'id_provincia',
                       'iddepartamento': 'id_departamento',
                       'direccion': 'domicilio',
                       'cp': 'código postal',
                       'telefono': 'número de teléfono'
                       }, inplace=True)
    df['categoría'] = category
    df_category = pd.DataFrame()
    headers = ['cod_localidad', 'id_provincia', 'id_departamento',
               'categoría', 'provincia', 'localidad', 'nombre',
               'domicilio', 'código postal', 'número de teléfono',
               'mail', 'web']
    for header in headers:
        df_category[header] = df[header]
    return df_category


def df_datos(categories: list[str]) -> pd.DataFrame():
    '''
    Obtiene el dataframe para la tabla datos
    '''
    df_datos = pd.DataFrame()
    for category in categories:
        df = df_category(category)
        df_datos = pd.concat([df_datos, df])
    return df_datos


def df_cines() -> pd.DataFrame():
    '''
    Obtiene el dataframe para la tabla cines
    '''
    df_cines = read_csv_normalize('cines')

    df_cines['espacio_incaa'] = df_cines['espacio_incaa'].fillna(0)
    df_cines['espacio_incaa'] = df_cines['espacio_incaa'].replace(['0'], 0)
    df_cines['espacio_incaa'] = df_cines['espacio_incaa'].replace(['si', 'SI'],
                                                                  1)

    headers = ['provincia', 'butacas', 'pantallas', 'espacio_incaa']
    for column in df_cines.columns:
        if column not in headers:
            df_cines = df_cines.drop([column], axis=1)

    # Agrupo por provincia
    df_cines = df_cines.groupby('provincia')
    df_cines = df_cines.sum()
    df_cines = df_cines.reset_index()
    return df_cines


def df_registros() -> pd.DataFrame():
    '''
    Obtiene el dataframe para la tabla registros
    '''
    df_registros = pd.DataFrame()
    categories = ['cines', 'bibliotecas', 'museos']

    for category in categories:
        df = read_csv_normalize(category)
        row = {'tipo_registro': 'categoria',
               'registro': category,
               'cant_registros': df.shape[0]}
        row = pd.DataFrame([row])
        df_registros = pd.concat([df_registros, row])

    for category in categories:
        df_category = read_csv_normalize(category)
        df_category_fuente = df_category.groupby('fuente')
        for name, group in df_category_fuente:
            row = {'tipo_registro': 'fuente',
                   'registro': name,
                   'cant_registros': group.shape[0]}
            row = pd.DataFrame([row])
            df_registros = pd.concat([df_registros, row])

    for category in categories:
        df_category = read_csv_normalize(category)
        df_category_prov = df_category.groupby('provincia')
        for name, group in df_category_prov:
            row = {'tipo_registro': 'categoria y provincia',
                   'registro': f'{category} / {name}',
                   'cant_registros': group.shape[0]}
            row = pd.DataFrame([row])
            df_registros = pd.concat([df_registros, row])

    return df_registros
