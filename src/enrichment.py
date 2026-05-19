# April 26, 2026. 3:30 p.m.
# This code enriches the dataset

import pandas, logging, os, json
from pathlib import Path
from dataclasses import dataclass

@dataclass
class Data:
    artists_dataframe: pandas.DataFrame
    albums_dataframe: pandas.DataFrame
    tracks_dataframe: pandas.DataFrame
    classifications: dict

logger = logging.getLogger("ENRICH")

def print_list(the_list):
    for item in the_list:
        print(f'{item['id']}. {item['name']}')

def define_classifications(data, classification_name):
    os.system('clear')
    print(f'We are accessing the database: \'{classification_name}\'')
    print('Commands:')
    print('\tp: Print existing data')
    print('\tw: Enter write mode')
    print('\td: Enter delete mode')
    print('\tq: Quit')

    while True:
        command = input('> ')

        if command == 'p':
            print_list(data.classifications[classification_name])
            continue

        elif command == 'd':
            print_list(data.classifications[classification_name])
            ids = sorted([
                int(id.strip())
                for id in input(f'Enter one or multiple id(s) to delete from the database: ').split(',')
                if id.strip() and int(id) < len(data.classifications[classification_name])
            ], reverse = True)
            for id in ids: data.classifications[classification_name].pop(id)
            continue

        elif command == 'q':
            os.system('clear')
            break

        elif command != 'w':
            input('Command doesn\'t exist! Try again...')
            continue

        classifications = [
            classification.strip()
            for classification in input(f'Enter one or multiple {classification_name}(s) to add to the database (Enter \'exit\' to stop) ').split(',')
            if classification.strip() and not any(item['name'] == classification for item in data.classifications[classification_name])
        ]

        for classification in classifications:
            data.classifications[classification_name].append({
                'id': len(data.classifications[classification_name]),
                'name': classification
            })

def get_artist_tracks(artist_id, data):
    logger.info('Querying artist tracks')

    artist_albums = data.albums_dataframe[data.albums_dataframe['artist_id'] == artist_id]
    album_ids = list(artist_albums['id'])
    track_ids = list()

    for album_id in album_ids:
        album_tracks = data.tracks_dataframe[data.tracks_dataframe['album_id'] == album_id]
        album_track_ids = list(album_tracks['id'])
        track_ids += album_track_ids
    
    return track_ids

def ask_track_classification(data, artist, classification_name, not_null):
    artist_classifications = [
        classification.strip()
        for classification in input(f'What {classification_name}(s) should {artist['name']} be? ').split(',')
        if classification.strip()
    ]

    logger.debug('Checking classification correctness')

    if len(artist_classifications) == 0 and not_null:
        logger.error(f'The {classification_name} cannot be empty! Try again')
        return -1

    for artist_classification in artist_classifications:
        query = any(item['name'] == artist_classification for item in data.classifications[classification_name])
        if not(query):
            logger.error(f'The value {artist_classification} is not valid as a {classification_name}! Try again')
            return -1

    return artist_classifications

def set_track_classifications(data, artist_tracks, artist_classifications, classification_name):
    track_classifications = list()

    for artist_track in artist_tracks:
        for artist_classification in artist_classifications:
            classification_index = next(
                item['id'] for item in data.classifications[classification_name]
                if item['name'] == artist_classification
            )

            track_classifications.append(
                {
                    'track_id': artist_track,
                    f'{classification_name}_id': classification_index
                }
            )
    
    return track_classifications

def get_track_classifications(data, classification_name, not_null = False):
    '''Assign a classification to the tracks cascading from an artist'''

    track_classifications = list()

    for artist_index in range(data.artists_dataframe.shape[0]):
        artist = data.artists_dataframe.iloc[artist_index]

        os.system('clear')

        artist_tracks = get_artist_tracks(artist['id'], data)
        artist_classifications = ask_track_classification(data, artist, classification_name, not_null)

        while artist_classifications == -1:
            artist_classifications = ask_track_classification(data, artist, classification_name, not_null)

        track_classifications += set_track_classifications(data, artist_tracks, artist_classifications, classification_name)
        
    return track_classifications

def write_data(target_path, data):
    for key in data.keys():
        logger.info(f'Transforming {key} into dataframe and storing in parquet format')
        dataframe = pandas.DataFrame(data[key])
        dataframe.to_parquet(f'{target_path}/{key}.parquet.gzip', compression = 'gzip')

def main(base_path, target_path):
    logger.info('Starting')
    logger.info('Loading data')

    subgenres_path = Path(f'{base_path}/subgenres.json')
    styles_path = Path(f'{base_path}/styles.json')

    with open(subgenres_path, 'r') as file: subgenres = json.load(file)
    with open(styles_path, 'r') as file: styles = json.load(file)

    data = Data (
        artists_dataframe = pandas.read_parquet(f'{target_path}/artists.parquet.gzip'),
        albums_dataframe = pandas.read_parquet(f'{target_path}/albums.parquet.gzip'),
        tracks_dataframe = pandas.read_parquet(f'{target_path}/tracks.parquet.gzip'),
        classifications = {
            'subgenres': subgenres,
            'styles': styles
        }
    )
    
    define_classifications(data, 'subgenres')
    define_classifications(data, 'styles')

    with open(subgenres_path, 'w') as file: json.dump(data.classifications['subgenres'], file)
    with open(styles_path, 'w') as file: json.dump(data.classifications['styles'], file)

    logger.info('Data loaded successfully. Ready to begin')
    input('Press ENTER to continue...')

    track_classifications = {
        'tracks_subgenres': get_track_classifications(data, 'subgenres', not_null = True),
        'tracks_styles': get_track_classifications(data, 'styles')
    }

    write_data(target_path, track_classifications)
    write_data(target_path, data.classifications)

def run(base_path, target_path):
    try:
        main(base_path, target_path)
        return 0
    except KeyboardInterrupt:
        logger.info('Exiting program')
        exit()
    except Exception as e:
        logger.critical(e)
        return -1

# April 26, 2026. 6:00 p.m. Finished
# May 18, 2026. 6:40 p.m. Refactoring Error Handling & Flow
# May 18, 2026. 9:00 p.m. Finished
