import sqlite3, csv, logging, sys, random
from pathlib import Path
import pandas as pd
import yaml

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


if __name__ == '__main__':

    # Load play accounts from configuration.yml
    try:
        accounts = yaml.safe_load(open('configuration.yml', 'r'))['simplelogin']['accounts']
    except Exception as e:
        print(e)

    dbname = 'winereviews.db'
    data_path = 'data/winemag-data_first150k.csv'
    Path(dbname).touch()

    try:
        df = pd.read_csv(data_path, index_col=0)
        df.index.name = 'id'
        df['private'] = [random.randint(0,1) for i in range(len(df))]
        df['user_published'] = [accounts[random.randint(0,len(accounts)-1)] for i in range(len(df))]
    except FileNotFoundError:
        logger.error(f'data not found at {data_path}')
    except Exception as e:
        logger.error(e)

    logger.debug(df.head())

    try:
        con = sqlite3.connect(dbname)
        df.to_sql('reviews', con, if_exists='replace')
    except Exception as e:
        logger.error('Unable to connect to db' + e)
        sys.exit(1)
