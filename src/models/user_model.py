import sqlite3

from . import constant
from src.services.logging_service import LoggingService

logging_service = LoggingService(name=__name__, formatter=None, datefmt=None, file_handler=None)

logger = logging_service.get_logger()


class Schema:
    def __init__(self, db_name=constant.DB_NAME):
        self.conn = sqlite3.connect(db_name)
        self.curs = self.conn.cursor()
        self.create_user_table()

    def __del__(self):
        self.conn.close()

    def create_user_table(self):
        query = """
                CREATE TABLE IF NOT EXISTS "user" (
                id INTEGER PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                username TEXT NOT NULL
                );
                """

        self.curs.execute(query)
        self.conn.commit()


class UserModel:
    def __init__(self, db_url=constant.DB_NAME):
        self.conn = sqlite3.connect(db_url)
        self.conn.row_factory = sqlite3.Row
        self.curs = self.conn.cursor()

    def create(self, id, first_name, last_name, username):
        query = """
                INSERT INTO user(id, first_name, last_name, username)
                VALUES(?, ?, ?, ?)
                """

        try:
            self.curs.execute(query, (id, first_name, last_name, username))
            self.conn.commit()

            return True
        except sqlite3.Warning as e:
            logger.exception("UserModel -> create -> Warning -> " + str(e))

            return False
        except sqlite3.Error as e:
            logger.exception("UserModel -> create -> Error -> " + str(e))

            return False

    def delete(self, id):
        query = """
                DELETE FROM user 
                WHERE id=?
                """

        try:
            self.curs.execute(query, (id,))
            self.conn.commit()

            return True
        except sqlite3.Warning as e:
            logger.exception("UserModel -> delete -> Warning -> " + str(e))

            return False
        except sqlite3.Error as e:
            logger.exception("UserModel -> delete -> Error -> " + str(e))

            return False

    def exist(self, id):
        query = """
                SELECT EXISTS (
                    SELECT username
                    FROM user 
                    WHERE id=?
                )
                """

        try:
            res = self.curs.execute(query, (id,)).fetchone()
            self.conn.commit()

            return bool(res[0])
        except sqlite3.Warning as e:
            logger.exception("UserModel -> delete -> Warning -> " + str(e))

            return False
        except sqlite3.Error as e:
            logger.exception("UserModel -> delete -> Error -> " + str(e))

            return False
