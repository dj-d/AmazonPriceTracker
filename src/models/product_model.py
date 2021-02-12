import sqlite3
from src.services.logging_service import LoggingService

logging_service = LoggingService(name=__name__, formatter=None, datefmt=None, file_handler=None)

logger = logging_service.get_logger()

DB_NAME = "bot.db"


class Schema:
    """
    Provide methods for db management
    """

    def __init__(self, db_name=DB_NAME):
        self.conn = sqlite3.connect(db_name)
        self.curs = self.conn.cursor()
        self.create_amazon_table()
        self.create_camel_table()

    def __del__(self):
        self.conn.close()

    def create_amazon_table(self):
        """
        Init amazon product table

        @return: void
        """

        query = """
                CREATE TABLE IF NOT EXISTS "amazon" (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                product_name TEXT NOT NULL,
                url TEXT NOT NULL,
                price REAL NOT NULL
                );
                """

        self.curs.execute(query)
        self.conn.commit()

    def create_camel_table(self):
        """
        Init camel product table

        @return: void
        """

        query = """
                CREATE TABLE IF NOT EXISTS "camel" (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                url TEXT NOT NULL,
                type TEXT NOT NULL,
                supplier TEXT NOT NULL,
                price REAL,
                FOREIGN KEY (id) REFERENCES amazon(id)
                );
                """

        self.curs.execute(query)
        self.conn.commit()


class AmazonModel:
    """
    Provide methods for Amazon product management
    """

    AMAZON_TABLE_NAME = "amazon"

    def __init__(self, db_url=DB_NAME):
        self.conn = sqlite3.connect(db_url)
        self.conn.row_factory = sqlite3.Row
        self.curs = self.conn.cursor()

    def create(self, chat_id, name, product_name, url, price):
        """
        Create a new product

        @param chat_id:
        @param name: Name of the product
        @param product_name: Name of the product on Amazon
        @param url: URL of the product
        @param price: Price of the product
        @return: True | False
        """

        query = """
                INSERT INTO amazon(chat_id, name, product_name, url, price)
                VALUES (?, ?, ?, ?, ?)
                """

        try:
            self.curs.execute(query, [chat_id, name, product_name, url, price])
            self.conn.commit()

            return True

        except Exception as e:
            logger.exception("AmazonModel -> create")

            return False

    def delete(self, chat_id, url):
        """
        Delete a product by the URL

        @param chat_id:
        @param url: URL of the product
        @return: True | False
        """

        query = """
                DELETE FROM amazon
                WHERE chat_id=? AND url=?
                """

        try:
            self.curs.execute(query, (chat_id, url))
            self.conn.commit()

            return True

        except Exception as e:
            logger.exception("AmazonModel -> delete")

            return False

    def get_info(self, chat_id):
        """
        Get name and price of products

        @param chat_id:
        @return: tuple(name, price) | False
        """

        query = """
                SELECT name, price
                FROM amazon
                WHERE chat_id=?
                """

        try:
            res = self.curs.execute(query, (chat_id,)).fetchall()
            self.conn.commit()

            return res

        except Exception as e:
            logger.exception("AmazonModel -> get_info")

            return False

    def get_name(self, chat_id, url):
        """
        Get name of a product by URL

        @param chat_id:
        @param url: URL of the product
        @return: Name of the product | False
        """

        query = """
                SELECT name
                FROM amazon
                WHERE chat_id=? AND url=?
                """

        try:
            res = self.curs.execute(query, (chat_id, url)).fetchone()
            self.conn.commit()

            return res[0]

        except Exception as e:
            logger.exception("AmazonModel -> get_name")

            return False

    def get_first_name(self, chat_id):
        """
        Get name at first row of table

        @param chat_id:
        @return: Name of the product | False
        """

        query = """
                SELECT name
                FROM amazon
                WHERE chat_id=?
                """

        try:
            res = self.curs.execute(query, (chat_id,)).fetchone()
            self.conn.commit()

            return res[0]

        except Exception as e:
            logger.exception("AmazonModel -> get_first_name")

            return False

    def get_price(self, chat_id, url):
        """
        Get price of a product by URL

        @param chat_id:
        @param url: URL of the product
        @return: Price of the product | False
        """

        query = """
                SELECT price
                FROM amazon
                WHERE chat_id=? AND url=?
                """

        try:
            res = self.curs.execute(query, (chat_id, url)).fetchone()
            self.conn.commit()

            return res[0]

        except Exception as e:
            logger.exception("AmazonModel -> get_price")

            return False

    def get_urls(self, chat_id):
        """
        Get all urls

        @param chat_id:
        @return: list(url) | False
        """

        query = """
                SELECT url
                FROM amazon
                WHERE chat_id=?
                """

        try:
            res = self.curs.execute(query, (chat_id,)).fetchall()
            self.conn.commit()

            return res

        except Exception as e:
            logger.exception("AmazonModel -> get_urls")

            return False

    def get_url_by_name(self, chat_id, name):
        """
        Get the URL by name

        @param chat_id:
        @param name: Name of the product
        @return: String | False
        """

        query = """
                SELECT url
                FROM amazon
                WHERE chat_id=? AND name=?
                """

        try:
            res = self.curs.execute(query, (chat_id, name)).fetchone()
            self.conn.commit()

            return res[0]

        except Exception as e:
            logger.exception("AmazonModel -> get_url_by_name")

            return False

    def update_name(self, chat_id, old_name, new_name):
        """
        Change name of a product

        @param chat_id:
        @param old_name: Current name
        @param new_name: New name
        @return: True | False
        """

        query = """
                UPDATE amazon
                SET name=?
                WHERE chat_id=? AND name=?
                """

        try:
            self.curs.execute(query, (new_name, chat_id, old_name))
            self.conn.commit()

            return True

        except Exception as e:
            logger.exception("AmazonModel -> update_name")

            return False

    def update_price(self, chat_id, url, new_price):
        """
        Update price of a product by URL

        @param chat_id:
        @param url: URL of the product
        @param new_price: New price of the product
        @return: True | False
        """

        query = """
                UPDATE amazon
                SET price=?
                WHERE chat_id=? AND url=?
                """

        try:
            self.curs.execute(query, (new_price, chat_id, url))
            self.conn.commit()

            return True

        except Exception as e:
            logger.exception("AmazonModel -> update_price")

            return False

    def check_name(self, chat_id, name):
        """
        Check if a name exists

        @param chat_id:
        @param name: Name of the product
        @return: True | False
        """

        query = """
                SELECT EXISTS (
                    SELECT name
                    FROM amazon
                    WHERE chat_id=? AND name=?
                )
                """

        try:
            res = self.curs.execute(query, (chat_id, name)).fetchone()
            self.conn.commit()

            return bool(res[0])

        except Exception as e:
            logger.exception("AmazonModel -> check_name")

            return False

    def check_url(self, chat_id, url):
        """
        Check if a URL exists

        @param chat_id:
        @param url: URL of the product
        @return: True | False
        """

        query = """
                SELECT EXISTS (
                    SELECT name
                    FROM amazon
                    WHERE chat_id=? AND url=?
                )
                """

        try:
            res = self.curs.execute(query, (chat_id, url)).fetchone()
            self.conn.commit()

            return bool(res[0])

        except Exception as e:
            logger.exception("AmazonModel -> check_url")

            return False

    def count_product(self, chat_id):
        """
        Count how many product there are into the table

        @param chat_id:
        @return: Number of rows | False
        """

        query = """
                SELECT COUNT(*)
                FROM amazon
                WHERE chat_id=?
                """

        try:
            res = self.curs.execute(query, (chat_id,)).fetchone()
            self.conn.commit()

            return res[0]

        except Exception as e:
            logger.exception("AmazonModel -> count_product")

            return False


class CamelModel:
    """
    Provide methods for camel product management in the table
    """

    CAMEL_TABLE_NAME = "camel"

    def __init__(self, db_url=DB_NAME):
        self.conn = sqlite3.connect(db_url)
        self.conn.row_factory = sqlite3.Row
        self.curs = self.conn.cursor()

    def create(self, chat_id, url, type, supplier, price):
        """
        Create a new product

        @param url: URL of the product on Amazon
        @param type: Type of price (Current, Highest, Lowest, Average)
        @param supplier: Supplier of the product
        @param price: Price of the product
        @return: True | False
        """

        query = """
                INSERT INTO camel(chat_id, url, type , supplier, price)
                VALUES (?, ?, ?, ?, ?)
                """

        try:
            self.conn.execute(query, (chat_id, url, type, supplier, float(price)))
            self.conn.commit()

            return True

        except Exception as e:
            logger.exception("CamelModel -> create")

            return False

    def delete(self, chat_id, url):
        """
        Delete a product by the URL

        @param chat_id:
        @param url: URL of the product
        @return: True | False
        """

        query = """
                DELETE FROM camel
                WHERE chat_id=? AND url=?
                """

        try:
            self.conn.execute(query, (chat_id, url))
            self.conn.commit()

            return True

        except Exception as e:
            logger.exception("CamelModel -> delete")

            return False

    def get_info(self, chat_id):
        """
        Get base information of products

        @param chat_id:
        @return: tuple(url, type, supplier, price) | False
        """

        query = """
                SELECT url, type, supplier, price
                FROM camel
                WHERE chat_id=?
                """

        try:
            res = self.curs.execute(query, (chat_id,)).fetchall()
            self.conn.commit()

            return res

        except Exception as e:
            logger.exception("CamelModel -> get_info")

            return False

    def get_price_info(self, chat_id, url):
        """
        Get product sellers info

        @param chat_id:
        @param url: URL of the product on Amazon
        @return: tuple(type, supplier, price) | False
        """

        query = """
                SELECT type, supplier, price
                FROM camel
                WHERE chat_id=? AND url=?
                """

        try:
            res = self.curs.execute(query, (chat_id, url)).fetchall()
            self.conn.commit()

            return res

        except Exception as e:
            logger.exception("CamelModel -> get_price_info")

            return False

    def get_urls(self, chat_id):
        """
        Get all urls without duplicates

        @param chat_id:
        @return: list() | False
        """

        query = """
                SELECT DISTINCT url
                FROM camel
                WHERE chat_id=?
                """

        try:
            res = self.curs.execute(query, (chat_id,)).fetchall()
            self.conn.commit()

            return res

        except Exception as e:
            logger.exception("CamelModel -> get_urls")

            return False

    def update_price(self, chat_id, url, type, supplier, new_price):
        """
        Update the price of a specific product from a specific seller

        @param chat_id:
        @param url: URL of product on Amazon
        @param type: Type of price (Current, Highest, Lowest, Average)
        @param supplier: Supplier of the product
        @param new_price: New price of the product
        @return: True | False
        """

        query = """
                UPDATE camel
                SET price=?
                WHERE chat_id=? AND url=? AND type=? AND supplier=? 
                """

        try:
            self.curs.execute(query, (new_price, chat_id, url, type, supplier))
            self.conn.commit()

            return True

        except Exception as e:
            logger.exception("CamelModel -> update_price")

            return False

    def check_url(self, chat_id, url):
        """
        Check if a URL exists

        @param chat_id:
        @param url: URL of the product
        @return: True | False
        """

        query = """
                SELECT EXISTS (
                    SELECT url
                    FROM camel
                    WHERE chat_id=? AND url=?
                )
                """

        try:
            res = self.curs.execute(query, (chat_id, url)).fetchone()
            self.conn.commit()

            return bool(res[0])

        except Exception as e:
            logger.exception("CamelModel -> check_url")

            return False

    def count_product(self, chat_id):
        """
        Count how many product there are in the db

        @param chat_id:
        @return: Number of rows | False
        """

        query = """
                SELECT COUNT(*)
                FROM camel
                WHERE chat_id=?
                """

        try:
            res = self.curs.execute(query, (chat_id,)).fetchone()
            self.conn.commit()

            return int(res[0] / 12)

        except Exception as e:
            logger.exception("CamelModel -> count_product")

            return False
