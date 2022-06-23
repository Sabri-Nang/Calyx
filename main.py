from decouple import config
from download_csv import save_csv
from process_data import df_data, df_cines

url_museos = config('URL_MUSEOS')
url_bibliotecas = config('URL_BIBLIOTECAS')
url_cines = config('URL_CINES')

save_csv(url_cines)
save_csv(url_museos)
save_csv(url_bibliotecas)

categories = ['cines', 'museos', 'bibliotecas']
df_data = df_data(categories)
print(df_data)

df_cines = df_cines()
print(df_cines)
