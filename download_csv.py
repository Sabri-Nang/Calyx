from xmlrpc.client import Boolean
import requests
import os
from datetime import date


def set_date():
    '''
    Retorno los formatos de las fechas para crear los directorios
    '''
    today = date.today()
    day = today.day
    month = today.month
    year = today.year
    months = {
                 1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril', 5: 'mayo',
                 6: 'junio', 7: 'julio', 8: 'agosto', 9: 'septiembre',
                 10: 'noviembre', 12: 'diciembre'
                 }
    date_now = f'{day}-{month}-{year}'
    year_month = f'{year}-{months[month]}'
    return date_now, year_month


def set_category(url: str) -> str:
    '''
    Retorna la categoría (str) según la url
    '''
    category = os.path.split(url)[1]
    if 'museos' in category:
        category = 'museos'
    elif 'cine' in category:
        category = 'cines'
    elif 'biblioteca' in category:
        category = 'bibliotecas'
    return category


def check_url(url: str) -> Boolean:
    '''
    Chequea la existencia de la url
    '''
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return True
        else:
            return False
    except Exception:
        # Loggear un error
        print('error: la url no existe')
        return False


def create_dir(url: str) -> str:
    '''
    Crea los directorios correspondientes según categoría y fecha.
    Devuelve el directorio en el cuál se descarga el archivo csv
    '''
    status = check_url(url)
    dir_dest = ""
    if status:
        date_now, year_month = set_date()
        category = set_category(url)

        try:
            os.mkdir(category)
        except Exception:
            # Agregar log info
            print('El directorio ya existe')

        try:
            os.mkdir(os.path.join(category, year_month))
        except Exception:
            # Agregar log info
            print('La ruta ya existe')

        try:
            os.mkdir(os.path.join(category, year_month,
                     f'{category}-{date_now}'))
        except Exception:
            # Agregar log info
            print('La ruta de fecha existe')

        dir_dest = os.path.join(category, year_month, f'{category}-{date_now}')

    else:
        # Logear error
        print('No es posible crear el directorio para la url solicitada, no existe')

    return dir_dest


def save_csv(url: str) -> None:
    '''
    Guarda los csv en el dorectorio correspondiente a su categoría y fecha de
    descarga
    '''
    if check_url(url):
        dir_dest = create_dir(url)
        file = os.path.split(url)[1]
        files = os.listdir(dir_dest)
        # Puedo agregar un msj en el logging q diga q se reemplaxo el archivo
        with open(os.path.join(dir_dest, file), 'wb') as f, \
                requests.get(url, stream=True) as r:
            for line in r.iter_lines():
                f.write(line+'\n'.encode())
        if file in files:
            # log info
            print(f'El archivo {file} se sobreescribió')
        else:
            # log info
            print(f'Se creo el archivo {file}')

    else:
        # Agregar logging error
        print("No se puede guardar csv de una ruta caida")
