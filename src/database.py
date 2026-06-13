# April 26, 2026. 10:00 p.m.
# This code builds and populates the PostgreSQL database

from sqlalchemy import create_engine, text
import os, logging, pandas
from dataclasses import dataclass

logger = logging.getLogger("DATABASE")

@dataclass
class Settings:
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    @classmethod
    def query_env(cls):
        return cls(
            DB_USER = os.getenv('DB_USER'),
            DB_PASS = os.getenv('DB_PASS'),
            DB_HOST = os.getenv('DB_HOST'),
            DB_PORT = os.getenv('DB_PORT'),
            DB_NAME = os.getenv('DB_NAME')
        )

def setup_database(data):
    setup_engine = create_engine (
        f'postgresql+psycopg2://{data.DB_USER}:{data.DB_PASS}@{data.DB_HOST}:{data.DB_PORT}/{data.DB_NAME}',
        isolation_level = 'AUTOCOMMIT'
    )

    with setup_engine.connect() as connection:
        with open('sql_scripts/create_tables.sql') as file:
            connection.execute(text(file.read()))

    setup_engine.dispose()

def check_database(data):
    logger.info('Checking database existence')

    init_engine = create_engine (
        f'postgresql+psycopg2://{data.DB_USER}:{data.DB_PASS}@{data.DB_HOST}:{data.DB_PORT}/postgres',
        isolation_level = 'AUTOCOMMIT'
    )

    with init_engine.connect() as connection:
        try:
            connection.execute(text(f'DROP DATABASE {data.DB_NAME}')) # For clean testing purposes
        except Exception as e:
            logger.error(e)

        query = connection.execute(text('SELECT * FROM pg_database')).all()
        database_names = [database_info[1] for database_info in query]

        if data.DB_NAME in database_names:
            logger.info('Database already exists')
            return

        logger.warning('Database does not exist. Creating')
        connection.execute(text(f'CREATE DATABASE {data.DB_NAME} ENCODING = UTF8'))

        try:
            setup_database(data)
            logger.info('Database created successfully')
        except Exception as e:
            logger.critical('A critical error happened while executing create_tables.sql and the transaction was rolled back.')
            logger.critical(e)
            raise e

    init_engine.dispose()

def main(base_path):
    logger.info('Loading environment data')

    data = Settings.query_env()

    check_database(data)

    logger.info('Connecting to PostgreSQL')

    db_engine = create_engine (
        f'postgresql+psycopg2://{data.DB_USER}:{data.DB_PASS}@{data.DB_HOST}:{data.DB_PORT}/{data.DB_NAME}',
        isolation_level = 'AUTOCOMMIT'
    )

    logger.info('Querying DataFrames')

    dependence_order = (
        'users',
        'artists',
        'albums',
        'tracks',
        'subgenres',
        'styles',
        'tags',
        'tracks_subgenres',
        'tracks_styles',
        'tracks_tags',
        'artist_scoring',
        'album_scoring',
        'track_scoring'
    )

    dataframe_names = sorted(
        [
            str(file.name).replace('.parquet.gzip', '')
            for file in base_path.iterdir() if file.is_file()
        ],
        key = dependence_order.index)
    dataframes = dict()

    for dataframe_name in dataframe_names:
        dataframes[dataframe_name] = None

    dataframe_total = len(dataframes.keys())

    logger.info(f'{dataframe_total} dataframes were found')

    for name_index, name in enumerate(dataframes.keys()):
        logger.info(f'Loading dataframe {name} ({name_index + 1} out of {dataframe_total})')
        dataframes[name] = pandas.read_parquet(f'{base_path}/{name}.parquet.gzip')

    logger.info('Dataframes loaded correctly')

    for dataframe_index, (name, dataframe) in enumerate(dataframes.items()):
        logger.info(f'Populating table {name} ({dataframe_index + 1} out of {dataframe_total})')
        dataframe.to_sql(name, db_engine, if_exists = 'append', index = False)
    
    logger.info('Tables populated correctly')

def run(base_path):
    try:
        main(base_path)
        return 0
    except Exception as e:
        logger.critical(e)
        return -1

# April 27, 2026. 12:45 p.m. Finished
# June 11, 2026. 5:40 p.m. Starting delicious bug fixing session
# June 11, 2026. 7:00 p.m. Finished
