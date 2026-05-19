# April 26, 2026. 12:10 a.m.
# This code extracts the relevant data form the JSON files and stores it in parquet format

import pandas, json, logging, time
from pathlib import Path, PurePath
from datetime import datetime

class InvalidDataError(Exception):
    def __init__(self, data):
        super().__init__(f'An invalid field value was found and the row will be discarded. {data}')

logger = logging.getLogger("NORMALIZE")

def load_batch_tracks(album_id, tracks_json):
    batch_tracks = list()

    for track in tracks_json['items']:
        if not(isinstance(track['id'], str)):
            raise InvalidDataError(f'Track ID: {track['id']}')
        
        if not(isinstance(track['track_number'], int)):
            raise InvalidDataError(f'Track Number: {track['track_number']}')
        
        if not(isinstance(track['name'], str)):
            raise InvalidDataError(f'Track Name: {track['name']}')

        batch_tracks.append(
            {
                'id': track['id'],
                'album_id': album_id,
                'track': track['track_number'],
                'name': track['name']
            }
        )
    
    return batch_tracks

def load_tracks(artist_path, album_id, artist_data):
    tracks_path = Path(f'{artist_path}/tracks')
    track_files = sorted([file for file in tracks_path.iterdir() if file.is_file()], key = lambda file: PurePath(file))
                
    track_batch_files = [file for file in track_files if str(file).startswith(f'{tracks_path}/tracks_{album_id}')]
    track_batches = len(track_batch_files)

    for track_batch_index, track_batch_file in enumerate(track_batch_files):
        logger.info(f'Track batch {track_batch_index + 1} out of {track_batches} - Loading and normalizing')

        with open(track_batch_file, 'r') as file:
            tracks_json = json.load(file)
        
        artist_data['tracks'] += load_batch_tracks(album_id, tracks_json)

def load_batch_albums(artist_path, artist_id, albums_json, artist_data):
    batch_albums = list()

    album_total = len(albums_json['items'])

    for album_index, album in enumerate(albums_json['items']):
        logger.info(f'Album {album_index + 1} out of {album_total} - Normalizing')

        if not(isinstance(album['id'], str)):
            raise InvalidDataError(f'Album Name: {album['id']}')

        if not(isinstance(artist_id, str)):
            raise InvalidDataError(f'Artist ID: {artist_id}')

        if not(isinstance(album['name'], str)):
            raise InvalidDataError(f'Album Name: {album['name']}')

        if not(isinstance(album['images'][0]['url'], str)):
            raise InvalidDataError(f'Album Cover URL: {album['images'][0]['url']}')

        if not(isinstance(album['release_date'], str)):
            raise InvalidDataError(f'Album Release Date: {album['release_date']}')

        if album['release_date_precision'] == 'year':
            match_string = '%Y'
        elif album['release_date_precision'] == 'month':
            match_string = '%Y-%m'
        elif album['release_date_precision'] == 'day':
            match_string = '%Y-%m-%d'

        try:
            datetime.strptime(album['release_date'], match_string)
        except:
            raise InvalidDataError(f'Album Release Date: {album['release_date']}')

        batch_albums.append (
            {
                'id': album['id'],
                'artist_id': artist_id,
                'name': album['name'],
                'cover': album['images'][0]['url'],
                'release': album['release_date']
            }
        )

        logger.info(f'Album {album_index + 1} out of {album_total} - Searching for track batches')

        load_tracks(artist_path, album['id'], artist_data)
    
    return batch_albums

def load_albums(artist_path, artist_id, artist_data):
    albums_path = Path(f'{artist_path}/albums')
    album_files = sorted([file for file in albums_path.iterdir() if file.is_file()], key = lambda file: PurePath(file))
    album_batches = len(album_files)

    for album_batch_index, album_batch_file in enumerate(album_files):
        logger.info(f'Album batch {album_batch_index + 1} out of {album_batches} - Loading')

        with open(album_batch_file, 'r') as file:
            albums_json = json.load(file)

        artist_data['albums'] += load_batch_albums(artist_path, artist_id, albums_json, artist_data)

def load_artist(artist_path, artist_id):
    artist_data = {
        'artists': list(),
        'albums': list(),
        'tracks': list()
    }

    artist_file = [file for file in artist_path.iterdir() if file.is_file()][0]

    with open(artist_file, 'r') as file:
        artist_json = json.load(file)

    if not(isinstance(artist_id, str)):
        raise InvalidDataError(f'Artist ID: {artist_id}')
    
    if not(isinstance(artist_json['name'], str)):
        raise InvalidDataError(f'Artist Name: {artist_json['name']}')
    
    if not(isinstance(artist_json['images'][0]['url'], str)):
        raise InvalidDataError(f'Artist Image URL: {artist_json['images'][0]['url']}')

    artist_data['artists'].append({
        'id': artist_id,
        'name': artist_json['name'],
        'picture': artist_json['images'][0]['url']
    })

    load_albums(artist_path, artist_id, artist_data)

    return artist_data

def write_data(target_path, data):
    for key in data.keys():
        logger.info(f'Transforming {key} into dataframe and storing in parquet format')
        dataframe = pandas.DataFrame(data[key])
        dataframe.to_parquet(f'{target_path}/{key}.parquet.gzip', compression = 'gzip')

def load_data(target_path):
    if len([file for file in target_path.iterdir() if file.is_file()]) == 0:
        data = {
            'artists': list(),
            'albums': list(),
            'tracks': list()
        }
    else:
        data = {
            'artists': pandas.read_parquet(f'{target_path}/artists.parquet.gzip').to_dict(orient = 'records'),
            'albums': pandas.read_parquet(f'{target_path}/albums.parquet.gzip').to_dict(orient = 'records'),
            'tracks': pandas.read_parquet(f'{target_path}/tracks.parquet.gzip').to_dict(orient = 'records')
        }

    return data

def main(base_path, target_path, status_path):
    logger.info('Starting')

    with open(status_path) as file:
        status_object = json.load(file)

    start_time = time.time()

    logger.info('Checking the existence of previously normalized data')

    data = load_data(target_path)

    logger.info('Retrieving list of artist IDs')

    with open(f'{base_path}/artist_ids.json', 'r') as file:
        artist_ids = json.load(file)
        total_artists = len(artist_ids)

    logger.info(f'The amount of artist IDs found was {total_artists}')

    for artist_index, artist_id in enumerate(artist_ids):
        logger.info(f'Artist {artist_id} ({artist_index + 1} out of {total_artists}) - Beginning')

        if status_object[artist_id]['ingestion'] != 'OK':
            logger.error(f'Artist {artist_id} appears with an status of: ingestion FAILED. Skipping')
            continue

        if status_object[artist_id]['normalization'] == 'OK':
            logger.info(f'Artist {artist_id} was already normalized. Skipping')
            continue

        artist_path = Path(f'{base_path}/artist_{artist_id}')

        if not(artist_path.exists()):
            logger.error(f'Artist {artist_id} ({artist_index + 1} out of {total_artists}) - Appears as OK but Not found in Datalake')
            continue

        try:
            artist_data = load_artist(artist_path, artist_id)
            for key in data.keys(): data[key] += artist_data[key]
            logger.info(f'Artist {artist_id} ({artist_index + 1} out of {total_artists}) - Completed Successfully')
            status_object[artist_id]['normalization'] = 'OK'

        except Exception as e:
            logger.error(f'Artist {artist_id} ({artist_index + 1} out of {total_artists}) - Failed')
            status_object[artist_id]['normalization'] = 'FAIL'
            logger.error(e)
            continue

        logger.info('Beginning to write data')

        write_data(target_path, data)
        with open(status_path, 'w') as file:
            json.dump(status_object, file)

    end_time = time.time()
    duration = end_time - start_time

    return duration

def run(base_path, target_path, status_path):
    try:
        main(base_path, target_path, status_path)
        return 0
    except Exception as e:
        logger.critical(e)
        return -1

# April 26, 2026. 02:00 a.m. Finished
# May 10, 2026. 6:30 p.m. Refactor & Improve Resumability
# April 26, 2026. 08:30 p.m. Break
# April 26, 2026. 08:40 p.m. Resume
# April 26, 2026. 09:00 p.m. Finished
