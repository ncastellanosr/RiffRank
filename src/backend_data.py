# June 12, 2026. 11:45 a.m.

from sqlalchemy import create_engine, text
import os, logging
from dotenv import load_dotenv
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime

load_dotenv()

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

class InvalidCredentials(Exception):
    def __init__(self):
        super().__init__(f'Unable to Log In')
    
class UserAlreadyExists(Exception):
    def __init__(self, username):
        super().__init__(f'User \'{username}\' already exists!')

logger = logging.getLogger("BACKEND")

def sign_up (username, password):
    data = Settings.query_env()
    engine = create_engine (
        f'postgresql+psycopg2://{data.DB_USER}:{data.DB_PASS}@{data.DB_HOST}:{data.DB_PORT}/{data.DB_NAME}',
        isolation_level = 'AUTOCOMMIT'
    )

    with engine.connect() as connection:
        result = connection.execute(text(
            f'SELECT * FROM users where username = \'{username}\''
        ))

        if len(result.all()) == 0:
            connection.execute(text(
                'INSERT INTO users (username, password) ' + \
                f'VALUES (\'{username}\', \'{password}\');'
            ))

            return 0

        raise UserAlreadyExists(username)

def log_in (username, password):
    data = Settings.query_env()
    engine = create_engine (
        f'postgresql+psycopg2://{data.DB_USER}:{data.DB_PASS}@{data.DB_HOST}:{data.DB_PORT}/{data.DB_NAME}',
        isolation_level = 'AUTOCOMMIT'
    )

    with engine.connect() as connection:
        result = connection.execute(text(
            f'SELECT password FROM users WHERE username = \'{username}\';'
        ))

        if result.first()[0] == password:
            return engine

        raise InvalidCredentials()

def list_artists (connection):
    result = connection.execute(text(
        'SELECT * FROM artists;'
    ))

    return result.all()

def list_artist (connection, artist_id):
    artist = connection.execute(text(
        f'SELECT * FROM artists WHERE id = \'{artist_id}\''
    )).all()[0]

    albums = connection.execute(text(
        f'SELECT * FROM artist WHERE artist_id = \'{artist_id}\';'
    )).all()

    return [artist, albums]

def list_album (connection, album_id):
    album = connection.execute(text(
        f'SELECT * FROM albums WHERE id = \'{album_id}\''
    )).all()[0]

    tracks = connection.execute(text(
        f'SELECT * FROM album WHERE album_id = \'{album_id}\';'
    )).all()

    return [album, tracks]

def rate_artist (connection, artist_id, username, score, tier = 0, favorite = False):
    result = connection.execute(text(
        f'SELECT * FROM artist_scoring WHERE artist_id = \'{artist_id}\' AND username = \'{username}\';'
    ))

    if len(result.all()) != 0:
        connection.execute(text(
            'UPDATE artist_scoring ' + \
            f'SET score = \'{score}\', tier = \'{tier}\', favorite = \'{favorite}\' ' + \
            f'WHERE artist_id = \'{artist_id}\' AND username = \'{username}\';'
        ))
    else:
        connection.execute(text(
            'INSERT INTO artist_scoring (artist_id, username, score, tier, favorite)' + \
            f'VALUES (\'{artist_id}\', \'{username}\', \'{score}\', \'{tier}\', \'{favorite}\');'
        ))

    return 0

def rate_album (connection, album_id, username, score, tier = 0, favorite = False):
    result = connection.execute(text(
        f'SELECT * FROM album_scoring WHERE album_id = \'{album_id}\' AND username = \'{username}\';'
    ))

    if len(result.all()) != 0:
        connection.execute(text(
            'UPDATE album_scoring ' + \
            f'SET score = \'{score}\', tier = \'{tier}\', favorite = \'{favorite}\' ' + \
            f'WHERE album_id = \'{album_id}\' AND username = \'{username}\';'
        ))
    else:
        connection.execute(text(
            'INSERT INTO album_scoring (album_id, username, score, tier, favorite)' + \
            f'VALUES (\'{album_id}\', \'{username}\', \'{score}\', \'{tier}\', \'{favorite}\');'
        ))

    return 0

def rate_track (connection, track_id, username, score, extended_score, tier = 0, favorite = False):
    result = connection.execute(text(
        f'SELECT * FROM track_scoring WHERE track_id = \'{track_id}\' AND username = \'{username}\';'
    ))

    if len(result.all()) != 0:
        connection.execute(text(
            'UPDATE track_scoring ' + \
            f'SET score = \'{score}\', tier = \'{tier}\', favorite = \'{favorite}\'' + \
            ''.join(f', {key} = \'{extended_score[key]}\'' for key in extended_score) + ' ' + \
            f'WHERE track_id = \'{track_id}\' AND username = \'{username}\';'
        ))
    else:
        connection.execute(text(
            'INSERT INTO track_scoring (track_id, username, score, tier, favorite' + \
            ''.join(f', {key}' for key in extended_score) + ')' + \
            f'VALUES (\'{track_id}\', \'{username}\', \'{score}\', \'{tier}\', \'{favorite}\'' + \
            ''.join(f', \'{extended_score[key]}\'' for key in extended_score) + ');'
        ))

    return 0

def get_artist_rating(connection, artist_id, username):
    result = connection.execute(text(
        f'SELECT * FROM artist_scoring WHERE artist_id = \'{artist_id}\' AND username = \'{username}\';'
    )).all()

    return result[0][2:] if len(result) > 0 else [5, 0, False]

def get_album_rating(connection, album_id, username):
    result = connection.execute(text(
        f'SELECT * FROM album_scoring WHERE album_id = \'{album_id}\' AND username = \'{username}\';'
    )).all()

    return result[0][2:] if len(result) > 0 else [5, 0, False]

def get_track_rating(connection, track_id, username):
    result = connection.execute(text(
        f'SELECT * FROM track_scoring WHERE track_id = \'{track_id}\' AND username = \'{username}\';'
    )).all()

    if len(result) > 0:
        row = result[0]
        return [row[2], {'melody': row[3], 'solo': row[4], 'vocals': row[5]}, row[6], row[7]]
    else:
        return [5, {'melody': 0, 'solo': 0, 'vocals': 0}, 0, False]

def main(action, engine = None, username = None, password = None):
    logs_path = Path(f'logs')
    logs_path.mkdir(exist_ok = True)

    logging.basicConfig (
        level = logging.INFO,
        format = '%(asctime)s %(name)s %(levelname)s %(message)s',
        handlers = [
            logging.FileHandler(f'{logs_path}/{datetime.now()}.log'),
            logging.StreamHandler()
        ]
    )

    if action == 'signup':
        logger.info('Creating Account')
        sign_up (username, password)
        return 0

    elif action == 'login':
        logger.info('Authenticating')
        return log_in (username, password)

    else:
        logger.info('Setting Up')
        functions = {
            'list_artists': list_artists,
            'list_artist': list_artist,
            'list_album': list_album,
            'rate_artist': rate_artist,
            'rate_album': rate_album,
            'rate_track': rate_track,
            'get_artist_rating': get_artist_rating,
            'get_album_rating': get_album_rating,
            'get_track_rating': get_track_rating
        }

        args = action[1:]

        logger.info('Connecting to the Database')
        with engine.engine.connect() as connection:
            return functions[action[0]](connection, *args)

def run(action, engine, username = None, password = None):
    try:
        return main (action, engine, username, password)
    except InvalidCredentials:
        logger.error('Invalid credentials!')
        return -2
    except Exception as e:
        logger.critical(e)
        return -1

"""
How to use:
    1) Create an user if necessary by calling run('signup', None, username, password)
    2) Obtain an engine object by calling run('login', None, username, password)
    3) Execute backend calls by calling run((funcname, *args), engine)

Function possibilities:
    list_artists: *args = ()
    list_artist: *args = (artist_id)
    list_album: *args = (album_id)
    rate_artist: *args = (artist_id, username, score, tier = 0, favorite = False)
    rate_album: *args = (album_id, username, score, tier = 0, favorite = False)
    rate_track: *args = (track_id, username, score, extended_scoring -> {'criteria': score, 'criteria': score}, tier = 0, favorite = False)
    get_artist_rating: *args = (artist_id, username)
    get_album_rating: *args = (album_id, username)
    get_track_rating: *args = (track_id, username)
"""

# June 12, 2026. 1:40 p.m. Finished
