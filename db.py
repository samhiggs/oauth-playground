import sqlite3, random
import pandas as pd

DBNAME='winereviews.db'

class SQLite:
    """Example of a contextmanager"""

    def __init__(self, file='winereviews.db'):
        self.file = file
    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        return self.conn.cursor()
    def __exit__(self, tpye, value, traceback):
        self.conn.close()

# Example of creating a custom exception name
class NotFoundError(Exception):
    pass

class NotAuthorizedError(Exception):
    pass

# You can also use decorators for retrying for the case where it might just
# be a random issue and retrying is solved.

# You can also create custom logging for exceptions with a logger.

def review_lst_to_json(item):
    return {
        "id": item[0],
        "country": item[1],
        "description": item[2],
        "designation": item[3],
        "points": item[4],
        "price": item[5],
        "province": item[6],
        "region_1": item[7],
        "region_2": item[8],
        "variety": item[9],
        "winery": item[10],
        "private": item[11],
        "user_published": item[12]
    }

def fetch_reviews(user: str = None):
    try:
        with SQLite('winereviews.db') as cur:
            # If user is none select 20 from a random start, otherwise only get users
            print(user)
            if user is None:
                qry = f"SELECT * FROM reviews where private=0 limit 20 offset {random.randint(0,10000)}"
            else:
                qry = f"SELECT * FROM reviews where private=0 and user_published = '{user}' limit 20"
            cur.execute(qry)
            result = list(map(review_lst_to_json, cur.fetchall()))
            return result

    except Exception as e:
        print(e)
        return []

def fetch_user_reviews(user: str):
    df = pd.DataFrame(fetch_reviews(user))
    return df.to_html()

def fetch_review(id: str):

    try:
        con = sqlite3.connect(DBNAME)
        cur = con.cursor()

        cur.execute(f"SELECT * FROM reviews where id={id}")
        result = cur.fetchone()

        if result is None:
            raise NotFoundError(f'Unable to find review with id {id}.')

        data = review_lst_to_json(result)

        if data['private']:
            raise NotAuthorizedError(f'You are not allowed to access review with id {id}')

        con.close()

        return data
    except sqlite3.OperationalError as e:
        print(e)
        raise NotFoundError(f'Unable to find review with id {id}.')
    finally:
        con.close()