# June 12, 2026. 11:45 a.m.

from sqlalchemy import create_engine, text
import os, logging, sys
from dotenv import load_dotenv
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime

load_dotenv()

logger = logging.getLogger("BACKEND LOW")

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
    def __init__(self, email):
        super().__init__(f'There is already an user linked to the email \'{email}\'!')

class BusyUsername(Exception):
    def __init__(self, username):
        super().__init__(f'The username \'{username}\' is already being used!')

def sign_up (email, username, password):
    logger.info('Executing Sign Up')
    logger.info('Setting Up')

    data = Settings.query_env()
    engine = create_engine (
        f'postgresql+psycopg2://{data.DB_USER}:{data.DB_PASS}@{data.DB_HOST}:{data.DB_PORT}/{data.DB_NAME}',
        isolation_level = 'AUTOCOMMIT'
    )

    logger.info('Connecting to the Database')

    with engine.connect() as connection:
        email_check = connection.execute(text(
            f'SELECT * FROM users WHERE email = \'{email}\''
        )).all()

        username_check = connection.execute(text(
            f'SELECT * FROM users WHERE username = \'{username}\''
        )).all()

        if len(email_check) != 0:
            raise UserAlreadyExists(email)

        if len(username_check) != 0:
            raise BusyUsername(username)

        connection.execute(text(
            'INSERT INTO users (email, username, password) ' + \
            f'VALUES (\'{email}\', \'{username}\', \'{password}\');'
        ))

        logger.info('Sign Up Finished Successfully')

        return 0

def log_in (username, password):
    logger.info('Executing Log In')
    logger.info('Setting Up')

    data = Settings.query_env()
    engine = create_engine (
        f'postgresql+psycopg2://{data.DB_USER}:{data.DB_PASS}@{data.DB_HOST}:{data.DB_PORT}/{data.DB_NAME}',
        isolation_level = 'AUTOCOMMIT'
    )

    logger.info('Connecting to the Database')

    with engine.connect() as connection:
        result = connection.execute(text(
            f'SELECT password FROM users WHERE username = \'{username}\';'
        )).first()

        if result is not None and result[0] == password:
            logger.info('Log In Finished Successfully')
            return engine

        raise InvalidCredentials()

def list_artists (connection):
    logger.info('Executing list_artists Query')

    result = connection.execute(text(
        'SELECT * FROM artists;'
    ))
    
    logger.info('list_artists Query was successful')

    return result.all()

def list_artist (connection, artist_id):
    logger.info('Executing list_artist Query')

    artist = connection.execute(text(
        f'SELECT * FROM artists WHERE id = \'{artist_id}\''
    )).all()[0]

    albums = connection.execute(text(
        f'SELECT * FROM artist WHERE artist_id = \'{artist_id}\';'
    )).all()

    logger.info('list_artist Query was successful')

    return [artist, albums]

def list_album (connection, album_id):
    logger.info('Executing list_album Query')

    album = connection.execute(text(
        f'SELECT * FROM albums WHERE id = \'{album_id}\''
    )).all()[0]

    tracks = connection.execute(text(
        f'SELECT * FROM album WHERE album_id = \'{album_id}\';'
    )).all()

    logger.info('list_album Query was successful')

    return [album, tracks]

def rate_artist (connection, artist_id, username, score, tier = 0, favorite = False):
    logger.info('Executing rate_artist Query')

    result = connection.execute(text(
        f'SELECT * FROM artist_scoring WHERE artist_id = \'{artist_id}\' AND username = \'{username}\';'
    ))

    if len(result.all()) != 0:
        logger.info('Artist already rated. Updating entry')

        connection.execute(text(
            'UPDATE artist_scoring ' + \
            f'SET score = \'{score}\', tier = \'{tier}\', favorite = \'{favorite}\' ' + \
            f'WHERE artist_id = \'{artist_id}\' AND username = \'{username}\';'
        ))
    else:
        logger.info('Artist not rated. Creating entry')

        connection.execute(text(
            'INSERT INTO artist_scoring (artist_id, username, score, tier, favorite)' + \
            f'VALUES (\'{artist_id}\', \'{username}\', \'{score}\', \'{tier}\', \'{favorite}\');'
        ))

    logger.info('rate_artist Query was successful')

    return 0

def rate_album (connection, album_id, username, score, tier = 0, favorite = False):
    logger.info('Executing rate_album Query')

    result = connection.execute(text(
        f'SELECT * FROM album_scoring WHERE album_id = \'{album_id}\' AND username = \'{username}\';'
    ))

    if len(result.all()) != 0:
        logger.info('Album already rated. Updating entry')

        connection.execute(text(
            'UPDATE album_scoring ' + \
            f'SET score = \'{score}\', tier = \'{tier}\', favorite = \'{favorite}\' ' + \
            f'WHERE album_id = \'{album_id}\' AND username = \'{username}\';'
        ))
    else:
        logger.info('Album not rated. Creating entry')

        connection.execute(text(
            'INSERT INTO album_scoring (album_id, username, score, tier, favorite)' + \
            f'VALUES (\'{album_id}\', \'{username}\', \'{score}\', \'{tier}\', \'{favorite}\');'
        ))

    logger.info('rate_album Query was successful')

    return 0

def rate_track (connection, track_id, username, score, extended_score, tier = 0, favorite = False):
    logger.info('Executing rate_track Query')

    result = connection.execute(text(
        f'SELECT * FROM track_scoring WHERE track_id = \'{track_id}\' AND username = \'{username}\';'
    ))

    if len(result.all()) != 0:
        logger.info('Track already rated. Updating entry')

        connection.execute(text(
            'UPDATE track_scoring ' + \
            f'SET score = \'{score}\', tier = \'{tier}\', favorite = \'{favorite}\'' + \
            ''.join(f', {key} = \'{extended_score[key]}\'' for key in extended_score) + ' ' + \
            f'WHERE track_id = \'{track_id}\' AND username = \'{username}\';'
        ))
    else:
        logger.info('Track not rated. Creating entry')

        connection.execute(text(
            'INSERT INTO track_scoring (track_id, username, score, tier, favorite' + \
            ''.join(f', {key}' for key in extended_score) + ')' + \
            f'VALUES (\'{track_id}\', \'{username}\', \'{score}\', \'{tier}\', \'{favorite}\'' + \
            ''.join(f', \'{extended_score[key]}\'' for key in extended_score) + ');'
        ))

    logger.info('rate_track Query was successful')

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

def search_artists(connection, search_string):
    result = connection.execute(text(
        f'SELECT * FROM artists WHERE LOWER(name) LIKE LOWER(\'%{search_string}%\')'
    )).all()

    return result

def search_albums(connection, search_string):
    result = connection.execute(text(
        f'SELECT * FROM albums WHERE LOWER(name) LIKE LOWER(\'%{search_string}%\')'
    )).all()

    return result

def search_tracks(connection, search_string):
    result = connection.execute(text(
        f'SELECT * FROM track WHERE LOWER(name) LIKE LOWER(\'%{search_string}%\')'
    )).all()

    return result

def get_user(connection, username):
    result = connection.execute(text(
        f'SELECT description FROM users WHERE username = \'{username}\''
    )).all()[0][0]

    return 'This bio is empty!' if result is None else result

def update_user(connection, current_username, new_username, bio):
    logger.info('Executing update_user Query')

    if bio is not None:
        logger.info('Reporting changes in description')
        connection.execute(text(
            'UPDATE users SET description = :bio WHERE username = :username'
        ), {'bio': bio, 'username': current_username})

    if new_username is not None:
        logger.info('Reporting changes in username')
        connection.execute(text(
            'UPDATE users SET username = :new_username WHERE username = :username'
        ), {'new_username': new_username, 'username': current_username})

def main(action, engine = None, email = None, username = None, password = None):
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
        sign_up (email, username, password)
        return 0

    elif action == 'login':
        logger.info('Authenticating')
        return log_in (username, password)

    else:
        logger.info('Performing Action')
        logger.info('Setting Up')
        func = getattr(sys.modules[__name__], action[0])
        args = action[1:]

        logger.info(f'Preparing to execute the function {func} with arguments {args}')

        logger.info('Connecting to the Database')
        with engine.engine.connect() as connection:
            return func(connection, *args)

def run(action, engine, email = None, username = None, password = None):
    try:
        result = main (action, engine, email, username, password)
        logger.info('Process exited successfully')
        return result
    except InvalidCredentials as e:
        logger.error(e)
        logger.info('Log In Did Not Finish Successfully')
        return -2
    except UserAlreadyExists as e:
        logger.error(e)
        logger.info('Sign Up Did Not Finish Successfully')
        return -3
    except BusyUsername as e:
        logger.error(e)
        logger.info('Sign Up Did Not Finish Successfully')
        return -4
    except Exception as e:
        logger.critical('An unknown error has occurred!')
        logger.critical(e)
        return -1

"""
How to use:
    1) Create an user if necessary by calling run('signup', None, email, username, password)
    2) Obtain an engine object by calling run('login', None, email, None, password)
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
    search_artists: *args = (search_string)
    search_albums: *args = (search_string)
    search_tracks: *args = (search_string)
    get_user: *args = (username)
    update_user: *args = (current_username, new_username = None, bio = None)
"""

# June 12, 2026. 1:40 p.m. Finished
