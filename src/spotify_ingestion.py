# April 24, 2026. 10:00 p.m.
# This code retrieves data from the Spotify API and stores raw payloads in JSON format

import os, time, logging, json, shutil, requests
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass

@dataclass
class Settings:
    base_url: str
    last_request: float | None = None
    session: requests.Session | None = None

class HTTPSessionError(Exception):
    def __init__(self, response_code):
        super().__init__(f'An error has occurred when trying to obtain a token to create an HTTP session. Response code: {response_code}')

class TokenRefreshError(Exception):
    def __init__(self, response_code):
        super().__init__(f'An error has occurred when trying refresh the session token. Response code: {response_code}')

class APIRequestError(Exception):
    def __init__(self, response_code):
        super().__init__(f'The API request was not possible: Reached maximum attempts. Response code: {response_code}')

logger = logging.getLogger("INGESTION")

def create_session():
    logger.debug('Loading environment variables')

    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')

    logger.info('Creating API session')

    session = requests.Session()

    response = session.post(
        'https://accounts.spotify.com/api/token',
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        data = {
            'grant_type': 'client_credentials',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
    )

    attempts = 3
    while attempts > 0:
        if response.status_code == 200:
            access_token = response.json()['access_token']
            session.headers.update({'Authorization': f'Bearer {access_token}'})
            logger.info('The API session was successfully created')
            return session
        else:
            attempts -= 1
            logger.error(f'The token couldn\'t be obtained when trying to create an HTTP session. Trying again ({attempts} attempts left)')

    raise HTTPSessionError(response.status_code)

def refresh_token(session):
    logger.debug('Loading environment variables')

    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')

    logger.info('Refreshing token')

    response = requests.post(
        'https://accounts.spotify.com/api/token',
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        data = {
            'grant_type': 'client_credentials',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
    )

    attempts = 3
    while attempts > 0:
        if response.status_code == 200:
            access_token = response.json()['access_token']
            session.headers.update({'Authorization': f'Bearer {access_token}'})
            logger.info('The token was successfully refreshed')
            return
        else:
            attempts -= 1
            logger.error(f'The token couldn\'t be refreshed. Trying again ({attempts} attempts left)')
    
    raise TokenRefreshError(response.status_code)

def request_cooldown(data):
    if data.last_request is None:
        data.last_request = time.time()
    else:
        time_elapsed = time.time() - data.last_request
        cooldown = 3

        if time_elapsed < cooldown:
            time_remaining = cooldown - time_elapsed
            logger.info(f'Waiting {time_remaining:.3f} seconds before the next request')
            time.sleep(time_remaining)

        data.last_request = time.time()

def format_time(seconds):
    f_hours = seconds // 3600
    f_minutes = (seconds % 3600) // 60
    f_seconds = seconds % 60

    return f'{f_hours}h{f_minutes}m{f_seconds}s'

def request_lobby(seconds):
    while seconds > 0:
        os.system('clear')
        print(f'Waiting {format_time(seconds)}')
        seconds -= 1
        time.sleep(1)

    os.system('clear')

    return 0

def spotify_request(endpoint, data):
    logger.debug('Beginning API request')

    attempts = 3
    while attempts > 0:
        response = data.session.get(f'{data.base_url}{endpoint}')

        if response.status_code == 200:
            logger.debug('The request was successful')
            return response

        elif response.status_code == 401:
            attempts -= 1
            logger.warning('The token has expired and needs to be refreshed')
            refresh_token(data.session)

        elif response.status_code == 429:
            wait_time = int(response.headers['retry-after'])
            
            logger.error('The rate limits have been exceeded')
            logger.info(f'The remaining wait time is {format_time(wait_time)}')

            attempts -= 1
            request_lobby(wait_time)
            logger.info('Wait time is over. Trying again')

    raise APIRequestError(response.status_code)

def request_artist_info (artist_id, data):
    request_cooldown(data)
    logger.info(f'Requesting info for artist {artist_id}')
    endpoint = f'/artists/{artist_id}'
    response = spotify_request(endpoint, data)

    logger.info(f'Info for artist {artist_id} was retrieved successfully')

    return response.json()

def request_album_tracks (album_id, data):
    limit = 50
    batch = 1

    endpoint = f'/albums/{album_id}/tracks'
    endpoint += f'?limit={limit}'

    responses = list()

    while True:
        request_cooldown(data)
        logger.info(f'Requesting tracks for album {album_id}, batch #{batch}, limit {limit}')

        response = spotify_request(endpoint, data)

        logger.info(f'Tracks for album {album_id}, batch #{batch}, limit {limit} were retrieved successfully')

        response_data = response.json()
        responses.append(response_data)

        if not response_data['next']:
            break

        batch += 1
        endpoint = response_data['next'].replace(data.base_url, '')

    return responses

def request_artist_albums (artist_id, data):
    limit = 10
    batch = 1

    endpoint = f'/artists/{artist_id}/albums'
    endpoint += '?include_groups=album'
    endpoint += f'&limit={limit}'

    responses = list()

    while True:
        request_cooldown(data)
        logger.info(f'Requesting albums for artist {artist_id}, batch #{batch}, limit {limit}')

        response = spotify_request(endpoint, data)
        
        logger.info(f'Albums for artist {artist_id}, batch #{batch}, limit {limit} were retrieved successfully')

        response_data = response.json()
        responses.append(response_data)

        if not response_data['next']:
            break

        batch += 1
        endpoint = response_data['next'].replace(data.base_url, '')

    return responses

def ingest_tracks(data, album_id, artist_path):
    tracks_path = Path(f'{artist_path}/tracks')
    tracks_path.mkdir(exist_ok = True)

    album_tracks = request_album_tracks(album_id, data)

    for tracks_index, tracks in enumerate(album_tracks):
        with open(f'{tracks_path}/tracks_{album_id}_{datetime.now()}_{tracks_index + 1}_of_{len(album_tracks)}.json', 'w') as file:
            json.dump(tracks, file)

def ingest_albums(data, artist_id, artist_path):
    albums_path = Path(f'{artist_path}/albums')
    albums_path.mkdir(exist_ok = True)

    artist_albums = request_artist_albums(artist_id, data)

    for albums_index, albums in enumerate(artist_albums):
        with open(f'{albums_path}/albums_{artist_id}_{datetime.now()}_{albums_index + 1}_of_{len(artist_albums)}.json', 'w') as file:
            json.dump(albums, file)

        for album in albums['items']:
            ingest_tracks(data, album['id'], artist_path)

def ingest_artist(artist_id, artist_path, data):
    logger.info('Setting up artist directory')

    if artist_path.is_dir():
        logger.warning('Artist directory already existed. Cleaning')
        shutil.rmtree(artist_path)

    artist_path.mkdir(exist_ok = True)

    artist_info = request_artist_info(artist_id, data)

    with open(f'{artist_path}/artist_{artist_id}_{datetime.now()}.json', 'w') as file:
        json.dump(artist_info, file)

    ingest_albums(data, artist_id, artist_path)

def main(base_path, status_path):
    logger.info('Starting')

    with open(status_path, 'r') as file:
        status_object = json.load(file)

    data = Settings (
        base_url = 'https://api.spotify.com/v1',
        session = create_session()
    )

    logger.info('Retrieving list of artist IDs')

    with open(f'{base_path}/artist_ids.json', 'r') as file:
        artist_ids = json.load(file)
        total_artists = len(artist_ids)

    logger.info(f'The amount of artist IDs found was {total_artists}')

    for artist_index, artist_id in enumerate(artist_ids):
        logger.info(f'Beginning ingestion for artist {artist_id} ({artist_index + 1} out of {total_artists})')

        if status_object[artist_id]['ingestion'] == 'OK':
            logger.info(f'Artist {artist_id} was already ingested. Skipping')
            continue

        artist_path = Path(f'{base_path}/artist_{artist_id}')
        
        try:
            ingest_artist(artist_id, artist_path, data)
            logger.info(f'Ingestion for artist {artist_id} was completed successfully ({artist_index + 1} out of {total_artists})')
            status_object[artist_id]['ingestion'] = 'OK'

        except Exception as e:
            logger.error(f'Ingestion for artist {artist_id} ({artist_index + 1} out of {total_artists}) failed unrecoverably')
            status_object[artist_id]['ingestion'] = 'FAIL'
            logger.warning(f'All progress for artist {artist_id} ({artist_index + 1} out of {total_artists}) will be deleted')
            shutil.rmtree(artist_path)
            raise(e)
        
        with open(status_path, 'w') as file:
            json.dump(status_object, file)

def run(base_path, status_path):
    try:
        main(base_path, status_path)
        return 0
    except Exception as e:
        logger.critical(e)
        return -1

# April 24, 2026. 11:00 p.m. Coffee Break
# April 24, 2026. 11:13 p.m. Resume
# April 25, 2026. 02:00 a.m. Finished
# May 10, 2026. 11:20 a.m. Refactoring Error Handling & Flow
# May 10, 2026. 2:30 p.m. Finished
