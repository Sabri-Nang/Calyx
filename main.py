from decouple import config
from download_csv import save_csv
from process_data import df_data, df_cines
from database import Database

url_museos = config('URL_MUSEOS')
url_bibliotecas = config('URL_BIBLIOTECAS')
url_cines = config('URL_CINES')

user = config('DB_USER')
password = config('DB_PASS')
host = config('DB_HOST_NAME')
port = config('DB_PORT')
database_name = config('DB_NAME')

save_csv(url_cines)
save_csv(url_museos)
save_csv(url_bibliotecas)

categories = ['cines', 'museos', 'bibliotecas']
df_data = df_data(categories)
print(df_data)

df_cines = df_cines()
print(df_cines)

# instancio base de datos
db = Database(user, password, host, port, database_name)
db.create_tables()
db.insert_data_from_df('cines', df_cines)
