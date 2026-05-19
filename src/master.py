# April 25, 2026. 8:40 p.m.
# This code orchestrates and synchronizes the program

import logging, json
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

import spotify_preload
import spotify_ingestion
import normalize
import enrichment
import database

@dataclass
class Settings:
    version: str

logger = logging.getLogger("MASTER")

if __name__ == '__main__':
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

    try:
        logger.info('Performing settings')

        data = Settings(version = '0.0.0')

        datalake_path = Path(f'raw_data/{data.version}')
        normalized_path = Path(f'normalized/{data.version}')

        datalake_path.mkdir(parents = True, exist_ok = True)
        normalized_path.mkdir(parents = True, exist_ok = True)

        status_path = Path(f'{logs_path}/status.json')
        subgenres_path = Path(f'{datalake_path}/subgenres.json')
        styles_path = Path(f'{datalake_path}/styles.json')

        if not(status_path.exists()):
            status_path.touch(exist_ok = True)
            status_object = dict()
            with open(status_path, 'w') as file:
                json.dump(status_object, file)
        
        if not(subgenres_path.exists()):
            subgenres_path.touch(exist_ok = True)
            subgenres = list()
            with open(subgenres_path, 'w') as file:
                json.dump(subgenres, file)

        if not(styles_path.exists()):
            styles_path.touch(exist_ok = True)
            styles = list()
            with open(styles_path, 'w') as file:
                json.dump(styles, file)

        auto_mode = input('Do you wish to perform the automatic mode? y/n: ')
        auto_mode = True if auto_mode == 'y' else False

        preload = 'y' if auto_mode else input('Do you wish to perform the preload? y/n: ')

        if preload == 'y':
            logger.info('Initiating preload program')
            spotify_preload.run(datalake_path, status_path)
            logger.info('Preload was successful')

        ingestion = 'y' if auto_mode else input('Do you wish to perform the ingestion? y/n: ')

        if ingestion == 'y':
            logger.info('Initiating ingestion program')
            spotify_ingestion.run(datalake_path, status_path)
            logger.info('Ingestion was successful')

        normalization = 'y' if auto_mode else input('Do you wish to perform the normalization? y/n: ')

        if normalization == 'y':
            logger.info('Initiating normalization program')
            duration = normalize.run(datalake_path, normalized_path, status_path)
            logger.info(f'Normalization was successfully completed in {duration:.3f}s')
        
        enrich = 'y' if auto_mode else input('Do you wish to perform the data enrichment? y/n: ')

        if enrich == 'y':
            logger.info('Initiating data enrichment program')
            enrichment.run(datalake_path, normalized_path)
            logger.info(f'Data enrichment was successful')
        
        database_setup = 'y' if auto_mode else input('Do you wish to perform the database setup? y/n: ')

        if database_setup == 'y':
            logger.info('Initiating database setup program')
            database.run(normalized_path)
            logger.info(f'Database setup was successful')

    except KeyboardInterrupt:
        logger.info('Exiting program')
        exit()
    
    except Exception as e:
        logger.critical(e)
        exit()

# April 25, 2026. 11:00 p.m. Finished
