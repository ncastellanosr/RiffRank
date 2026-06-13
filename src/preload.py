# April 24, 2026. 8:00 p.m.
# This code gathers the ID for each of the artists followed by the user

import os, logging, spotipy, json
from spotipy.oauth2 import SpotifyOAuth

logger = logging.getLogger("PRELOAD")

def main(base_path, status_path):
    logger.info('Starting')
    logger.debug('Loading environment variables')

    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    REDIRECT_URI = os.getenv('REDIRECT_URI')

    logger.info('Creating API session')

    session = spotipy.Spotify (
        auth_manager = SpotifyOAuth (
            client_id = CLIENT_ID,
            client_secret = CLIENT_SECRET,
            redirect_uri = REDIRECT_URI,
            scope = 'user-follow-read',
            open_browser = False
        )
    )

    session.current_user_followed_artists(limit = 1)
    
    logger.info('Preparing artist IDs retrieval')

    artist_ids = list()
    status = dict()
    batch = 1

    logger.info(f'Retrieving batch #{batch}')

    response = session.current_user_followed_artists(limit = 50)

    while response:
        for artist in response['artists']['items']:
            artist_ids.append(artist['id'])
            status[artist['id']] = {
                'ingestion': 'PENDING',
                'normalization': 'PENDING'
            }
        
        if not response['artists']['next']:
            break
        
        batch += 1

        logger.info(f'Retrieving batch #{batch}')
        response = session.next(response['artists'])
        
    logger.info('Writing data to file')

    with open(f'{base_path}/artist_ids.json', 'w') as file:
        json.dump(artist_ids, file)
    
    with open(f'{status_path}', 'w') as file:
        json.dump(status, file)
        
    logger.info('Cleaning')

    if os.path.isfile('.cache'):
        os.remove('.cache')
        
    logger.info('All operations were completed successfully')

def run(base_path, status_path):
    try:
        main(base_path, status_path)
        return 0
    except KeyboardInterrupt:
        logger.info('Exiting program')
        exit()
    except Exception as e:
        logger.critical(e)
        return -1

# April 24, 2026. 9:00 p.m. Finished
