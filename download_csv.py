from xmlrpc.client import Boolean
import requests
import os
from datetime import date
from logger import logger


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
        logger.error("La url no existe")
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
            logger.info(f"Se creó el directorio {category}")
        except Exception:
            logger.info(f"El directorio {category} ya existe")

        try:
            os.mkdir(os.path.join(category, year_month))
            logger.info(f"Se creó el subdirectorio {year_month} en {category}")
        except Exception:
            logger.info(f"La ruta {os.path.join(category, year_month)}\
             ya existe")

        try:
            os.mkdir(os.path.join(category, year_month,
                     f'{category}-{date_now}'))
            logger.info(f"Se creó el subdirectorio {category}-{date_now}\
                en {year_month}")
        except Exception:
            logger.info(f"El subdirectorio {category}-{date_now} ya existe")

        dir_dest = os.path.join(category, year_month, f'{category}-{date_now}')

    else:
        logger.error("La url solicitada no existe")

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
        with open(os.path.join(dir_dest, file), 'wb') as f, \
                requests.get(url, stream=True) as r:
            for line in r.iter_lines():
                f.write(line+'\n'.encode())
        if file in files:
            logger.info(f'El archivo {file} se sobreescribió')
        else:
            logger.info(f'Se creo el archivo {file}')

    else:
        logger.error("No se puede guardar csv de una ruta caida")
