import pymysql

def get_db():
    db = get_connection()

    try:
        yield db  # get database connection and give it to the endpoint and wait until the endpoint fineshes it's operation..
    finally:
        db.close()

from Backend.config import (
    DB_HOST,
    DB_USER,
    DB_PASSWORD,
    DB_DATABASE
)


def get_connection():

    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE,
        cursorclass=pymysql.cursors.DictCursor
    )
