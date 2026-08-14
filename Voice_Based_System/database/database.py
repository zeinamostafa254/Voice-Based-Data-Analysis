'''import sqlite3
from pathlib import Path  #this file handles the database connection and operations (SQLite)

BASE_DIR = Path(__file__).resolve().parent.parent #finding the project directory

DATA_DIR = BASE_DIR / "data"   #data directory
DATABASE_PATH = DATA_DIR / "database.db" # database path


DATA_DIR.mkdir(exist_ok=True)  # create the file database.db if it does not exist, and if it exists it doesnot throw an error due to the line (exist_ok = True)


def get_connection():  # create a connection to SQLite
    """
    Create and return a connection to the SQLite database.
    """

    connection = sqlite3.connect(
        DATABASE_PATH,
        check_same_thread=False
    )

    return connection


def get_table_schema(table_name="dataset"):
    """
    Return information about the columns in a table.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        f"PRAGMA table_info({table_name})"
    )

    columns = cursor.fetchall()

    connection.close()

    return columns'''

#new

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(exist_ok=True)

DATABASE_PATH = DATA_DIR / "database.db"


def get_connection():

    return sqlite3.connect(
        DATABASE_PATH,
        check_same_thread=False
    )


def get_table_schema(table_name="dataset"):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        f"PRAGMA table_info({table_name})"
    )

    columns = cursor.fetchall()

    connection.close()

    return columns