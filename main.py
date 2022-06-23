from decouple import config
from download_csv import save_csv

url_museos = config('URL_MUSEOS')
url_bibliotecas = config('URL_BIBLIOTECAS')
url_cines = config('URL_CINES')

save_csv(url_cines)
# save_csv(url_museos)
# save_csv(url_bibliotecas)
