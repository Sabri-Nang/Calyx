from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from logger import logger


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
        self.url_database = f"postgresql://{user}:{password}@{host}:{port}/\
                             {database_name}"

    def create_tables(self):
        if not database_exists(self.url_database):
            create_database(self.url_database)
            logger.info("Creando base de datos  {database_name}")
        try:
            engine = create_engine(self.url_database, echo=False)
            Session = sessionmaker(engine)
            session = Session()
            connection = engine.connect()
            logger.info("Conectado a la base de datos")
        except Exception:
            logger.error("No se puede conectar a la base de datos")
            return
        with open('tables_sql/datos.sql') as f:
            read_f = f.read()
            connection.execute(read_f)
            logger.info("Creada tabla datos.sql")
        with open('tables_sql/cines.sql') as f:
            read_f = f.read()
            connection.execute(read_f)
            logger.info("Creada tabla cines.sql")
        with open('tables_sql/registros.sql') as f:
            connection.execute(read_f)
            logger.info("Creada tabla registros.sql")
        session.commit()

    def insert_data_from_df(self, name_table, data_frame):
        engine = create_engine(self.url_database, echo=False)
        with engine.begin() as connection:
            data_frame['fecha_carga'] = datetime.datetime.now()
            data_frame.to_sql(name_table, connection,
                              if_exists='replace', index=False)
