import sqlite3
from src.services.logging_service import LoggingService

logging_service = LoggingService(name=__name__, formatter=None, datefmt=None, file_handler=None)

logger = logging_service.get_logger()

DB_NAME = "bot.db"


class Schema:
    def __init__(self, db_name=DB_NAME):
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
    USER_TABLE_NAME = "user"

    def __init__(self, db_url=DB_NAME):
        self.conn = sqlite3.connect(db_url)
        self.conn.row_factory = sqlite3.Row
        self.curs = self.conn.cursor()

    def create(self, id, first_name, last_name, username):
        query = """
                INSERT INTO user(id, fist_name, last_name, username)
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
        except sqlite3.IntegrityError as e:
            logger.exception("UserModel -> create -> IntegrityError -> " + str(e))

            return False
        except sqlite3.ProgrammingError as e:
            logger.exception("UserModel -> create -> ProgrammingError -> " + str(e))

            return False
        except sqlite3.OperationalError as e:
            logger.exception("UserModel -> create -> OperationalError -> " + str(e))

            return False
        except sqlite3.NotSupportedError as e:
            logger.exception("UserModel -> create -> NotSupportedError -> " + str(e))

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
        except sqlite3.IntegrityError as e:
            logger.exception("UserModel -> delete -> IntegrityError -> " + str(e))

            return False
        except sqlite3.ProgrammingError as e:
            logger.exception("UserModel -> delete -> ProgrammingError -> " + str(e))

            return False
        except sqlite3.OperationalError as e:
            logger.exception("UserModel -> delete -> OperationalError -> " + str(e))

            return False
        except sqlite3.NotSupportedError as e:
            logger.exception("UserModel -> delete -> NotSupportedError -> " + str(e))

            return False
