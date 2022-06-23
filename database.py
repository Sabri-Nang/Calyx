from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime


class Database:
    def __init__(self, user: str,
                 password: str,
                 host: str,
                 port: str,
                 database_name: str) -> None:
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database_name = database_name
        self.url_database = f"postgresql://{user}:{password}@{host}:{port}/{database_name}"

    def get_engine(user, password, host, port, database_name):    
        url_database = f"postgresql://{user}:{password}@{host}:{port}/{database_name}"
        if not database_exists(url_database):
            create_database(url_database)
        engine = create_engine(url_database, echo=False)
        return engine

    def create_tables(self):
        if not database_exists(self.url_database):
            create_database(self.url_database)
            print("Creando base de datos")
        engine = create_engine(self.url_database, echo=False)
        Session = sessionmaker(engine)
        session = Session()
        connection = engine.connect()
        print('Crar tabla')
        with open('tables_sql/datas.sql') as f:
            read_f = f.read()
            connection.execute(read_f)
            print("Creada tabla datas")
        with open('tables_sql/cines.sql') as f:
            read_f = f.read()
            connection.execute(read_f)
            print("Creada tabla cines")
        # Agregar la tercer tabla que me falta
        session.commit()

    def insert_data_from_df(self, name_table, data_frame):
        engine = create_engine(self.url_database, echo=False)
        with engine.begin() as connection:
            data_frame['fecha_carga'] = datetime.datetime.now()
            data_frame.to_sql(name_table, connection,
                              if_exists='replace', index=False)
