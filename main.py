from decouple import config
from download_csv import save_csv
import process_data
from database import Database


def main():
    SETTINGS = ['URL_MUSEOS', 'URL_BIBLIOTECAS', 'URL_CINES',
                'DB_USER', 'DB_PASS', 'DB_HOS_NAME', 'DB_NAME']

    for setting in SETTINGS:
        try:
            config(setting)
        except Exception:
            print('No se ha establecido {setting} en el archivo settings.ini')
            return

    url_museos = config('URL_MUSEOS')
    url_bibliotecas = config('URL_BIBLIOTECAS')
    url_cines = config('URL_CINES')

    user = config('DB_USER')
    password = config('DB_PASS')
    host = config('DB_HOST_NAME')
    port = config('DB_PORT')
    database_name = config('DB_NAME')

    # Guardo los csv
    save_csv(url_cines)
    save_csv(url_museos)
    save_csv(url_bibliotecas)

    # Creo dataframes correspondientes a las tablas
    categories = ['cines', 'museos', 'bibliotecas']
    df_datos = process_data.df_datos(categories)
    df_cines = process_data.df_cines()
    df_registros = process_data.df_registros()

    # Instancio base de datos
    db = Database(user, password, host, port, database_name)
    db.create_tables()

    # Inserto dataframe en las tablas
    db.insert_data_from_df('cines', df_cines)
    db.insert_data_from_df('datos', df_datos)
    db.insert_data_from_df('registros', df_registros)


main()
