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


def df_category(category):
    '''
    Normaliza el csv de la category y devuelve un dataframe con
    las columnas que
    interesan. Agrega una columna según la categoría
    '''
    file = get_last_csv(category)
    df = pd.read_csv(file)
    df.columns = [normalize_headers(column) for column in df.columns]
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


def df_data(categories: list[str]) -> pd.DataFrame():
    df_data = pd.DataFrame()
    for category in categories:
        df = df_category(category)
        df_data = pd.concat([df_data, df])
    return df_data


def df_cines():
    file = get_last_csv('cines')
    df_cines = pd.read_csv(file)
    df_cines.columns = [normalize_headers(column)
                        for column in df_cines.columns]

    df_cines['espacio_incaa'] = df_cines['espacio_incaa'].fillna(0)
    df_cines['espacio_incaa'] = df_cines['espacio_incaa'].replace(['0'], 0)
    df_cines['espacio_incaa'] = df_cines['espacio_incaa'].replace(['si', 'SI'],
                                                                  1)

    headers = ['provincia', 'butacas', 'pantallas', 'espacio_incaa']
    for column in df_cines.columns:
        if column not in headers:
            df_cines = df_cines.drop([column], axis=1)

    # Agrupo por provincia
    df_cines = df_cines.groupby('provincia').sum()
    return df_cines
