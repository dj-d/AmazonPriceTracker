import mysql.connector as mysql
from database.database import Database

from services.logging_service import LoggingService

logging_service = LoggingService(name=__name__, formatter=None, datefmt=None, file_handler=None)

logger = logging_service.get_logger()


class Schema:
    """
    Provide methods for db management
    """

    def __init__(self):
        self.conn = Database().get_conn()
        self.curs = self.conn.cursor()

        self.create_amazon_table()
        self.create_camel_table()

    def __del__(self):
        self.conn.close()

    # TODO: To change
    def create_amazon_table(self):
        """
        Init amazon product table

        @return: void
        """

        query = """
                CREATE TABLE IF NOT EXISTS "amazon" (
                name TEXT NOT NULL,
                product_name TEXT NOT NULL,
                url TEXT NOT NULL UNIQUE PRIMARY KEY,
                price REAL NOT NULL
                );
                """

        self.curs.execute(query)
        self.conn.commit()

    # TODO: To change
    def create_camel_table(self):
        """
        Init camel product table

        @return: void
        """

        query = """
                CREATE TABLE IF NOT EXISTS "camel" (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                type TEXT NOT NULL,
                supplier TEXT NOT NULL,
                price REAL,
                FOREIGN KEY (url) REFERENCES amazon(url)
                );                
                """

        self.curs.execute(query)
        self.conn.commit()


class AmazonModel:
    """
    Provide methods for Amazon product management
    """

    def __init__(self):
        self.conn = Database().get_conn()
        self.curs = self.conn.cursor()

    # TODO: To change
    def create(self, name, product_name, url, price):
        """
        Create a new product

        @param name: Name of the product
        @param product_name: Name of the product on Amazon
        @param url: URL of the product
        @param price: Price of the product
        @return: True | False
        """

        query = """
                INSERT INTO amazon(name, product_name, url, price)
                VALUES (?, ?, ?, ?)
                """

        try:
            self.curs.execute(query, [name, product_name, url, price])
            self.conn.commit()

            return True

        except Exception as e:
            logger.exception("AmazonModel -> create")

            return False

    # TODO: To change
    def delete(self, url):
        """
        Delete a product by the URL

        @param url: URL of the product
        @return: True | False
        """

        query = """
                DELETE FROM amazon
                WHERE url=?
                """

        try:
            self.curs.execute(query, (url,))
            self.conn.commit()

            return True

        except Exception as e:
            logger.exception("AmazonModel -> delete")

            return False

    # TODO: To change
    def get_info(self):
        """
        Get name and price of products

        @return: tuple(name, price) | False
        """

        query = """
                SELECT name, price
                FROM amazon
                """

        try:
            res = self.curs.execute(query).fetchall()
            self.conn.commit()

            return res

        except Exception as e:
            logger.exception("AmazonModel -> get_info")

            return False

    # TODO: To change
    def get_name(self, url):
        """
        Get name of a product by URL

        @param url: URL of the product
        @return: Name of the product | False
        """

        query = """
                SELECT name
                FROM amazon
                WHERE url=?
                """

        try:
            res = self.curs.execute(query, (url,)).fetchone()
            self.conn.commit()

            return res[0]

        except Exception as e:
            logger.exception("AmazonModel -> get_name")

            return False

    # TODO: To change
    def get_first_name(self):
        """
        Get name at first row of table

        @return: Name of the product | False
        """

        query = """
                SELECT name
                FROM amazon
                """

        try:
            res = self.curs.execute(query).fetchone()
            self.conn.commit()

            return res[0]

        except Exception as e:
            logger.exception("AmazonModel -> get_first_name")

            return False

    # TODO: To change
    def get_price(self, url):
        """
        Get price of a product by URL

        @param url: URL of the product
        @return: Price of the product | False
        """

        query = """
                SELECT price
                FROM amazon
                WHERE url=?
                """

        try:
            res = self.curs.execute(query, (url,)).fetchone()
            self.conn.commit()

            return res[0]

        except Exception as e:
            logger.exception("AmazonModel -> get_price")

            return False

    # TODO: To change
    def get_urls(self):
        """
        Get all urls

        @return: list(url) | False
        """

        query = """
                SELECT url
                FROM amazon
                """

        try:
            res = self.curs.execute(query).fetchall()
            self.conn.commit()

            return res

        except Exception as e:
            logger.exception("AmazonModel -> get_urls")

            return False

    # TODO: To change
    def get_url_by_name(self, name):
        """
        Get the URL by name

        @param name: Name of the product
        @return: String | False
        """

        query = """
                SELECT url
                FROM amazon
                WHERE name=?
                """

        try:
            res = self.curs.execute(query, (name,)).fetchone()
            self.conn.commit()

            return res[0]

        except Exception as e:
            logger.exception("AmazonModel -> get_url_by_name")

            return False

    # TODO: To change
    def update_name(self, old_name, new_name):
        """
        Change name of a product

        @param old_name: Current name
        @param new_name: New name
        @return: True | False
        """

        query = """
                UPDATE amazon
                SET name=?
                WHERE name=?
                """

        try:
            self.curs.execute(query, (new_name, old_name))
            self.conn.commit()

            return True

        except Exception as e:
            logger.exception("AmazonModel -> update_name")

            return False

    # TODO: To change
    def update_price(self, url, new_price):
        """
        Update price of a product by URL

        @param url: URL of the product
        @param new_price: New price of the product
        @return: True | False
        """

        query = """
                UPDATE amazon
                SET price=?
                WHERE url=?
                """

        try:
            self.curs.execute(query, (new_price, url))
            self.conn.commit()

            return True

        except Exception as e:
            logger.exception("AmazonModel -> update_price")

            return False

    # TODO: To change
    def check_name(self, name):
        """
        Check if a name exists

        @param name: Name of the product
        @return: True | False
        """

        query = """
                SELECT EXISTS (
                    SELECT name
                    FROM amazon
                    WHERE name=?
                )
                """

        try:
            res = self.curs.execute(query, (name,)).fetchone()
            self.conn.commit()

            return bool(res[0])

        except Exception as e:
            logger.exception("AmazonModel -> check_name")

            return False

    # TODO: To change
    def check_url(self, url):
        """
        Check if a URL exists

        @param url: URL of the product
        @return: True | False
        """

        query = """
                SELECT EXISTS (
                    SELECT name
                    FROM amazon
                    WHERE url=?
                )
                """

        try:
            res = self.curs.execute(query, (url,)).fetchone()
            self.conn.commit()

            return bool(res[0])

        except Exception as e:
            logger.exception("AmazonModel -> check_url")

            return False

    # TODO: To change
    def count_product(self):
        """
        Count how many product there are into the table

        @return: Number of rows | False
        """

        query = """
                SELECT COUNT(*)
                FROM amazon
                """

        try:
            res = self.curs.execute(query).fetchone()
            self.conn.commit()

            return res[0]

        except Exception as e:
            logger.exception("AmazonModel -> count_product")

            return False


class CamelModel:
    """
    Provide methods for camel product management in the table
    """

    def __init__(self):
        self.conn = Database().get_conn()
        self.curs = self.conn.cursor()

    # TODO: To change
    def create(self, url, type, supplier, price):
        """
        Create a new product

        @param url: URL of the product on Amazon
        @param type: Type of price (Current, Highest, Lowest, Average)
        @param supplier: Supplier of the product
        @param price: Price of the product
        @return: True | False
        """

        query = """
                INSERT INTO camel(url, type , supplier, price)
                VALUES (?, ?, ?, ?)
                """

        try:
            self.conn.execute(query, (url, type, supplier, float(price)))
            self.conn.commit()

            return True

        except Exception as e:
            logger.exception("CamelModel -> create")

            return False

    # TODO: To change
    def delete(self, url):
        """
        Delete a product by the URL

        @param url: URL of the product
        @return: True | False
        """

        query = """
                DELETE FROM camel
                WHERE url=?
                """

        try:
            self.conn.execute(query, (url,))
            self.conn.commit()

            return True

        except Exception as e:
            logger.exception("CamelModel -> delete")

            return False

    # TODO: To change
    def get_info(self):
        """
        Get base information of products

        @return: tuple(url, type, supplier, price) | False
        """

        query = """
                SELECT url, type, supplier, price
                FROM camel
                """

        try:
            res = self.curs.execute(query).fetchall()
            self.conn.commit()

            return res

        except Exception as e:
            logger.exception("CamelModel -> get_info")

            return False

    # TODO: To change
    def get_price_info(self, url):
        """
        Get product sellers info

        @param url: URL of the product on Amazon
        @return: tuple(type, supplier, price) | False
        """

        query = """
                SELECT type, supplier, price
                FROM camel
                WHERE url=?
                """

        try:
            res = self.curs.execute(query, (url,)).fetchall()
            self.conn.commit()

            return res

        except Exception as e:
            logger.exception("CamelModel -> get_price_info")

            return False

    # TODO: To change
    def get_urls(self):
        """
        Get all urls without duplicates

        @return: list() | False
        """

        query = """
                SELECT DISTINCT url
                FROM camel
                """

        try:
            res = self.curs.execute(query).fetchall()
            self.conn.commit()

            return res

        except Exception as e:
            logger.exception("CamelModel -> get_urls")

            return False

    # TODO: To change
    def update_price(self, url, type, supplier, new_price):
        """
        Update the price of a specific product from a specific seller

        @param url: URL of product on Amazon
        @param type: Type of price (Current, Highest, Lowest, Average)
        @param supplier: Supplier of the product
        @param new_price: New price of the product
        @return: True | False
        """

        query = """
                UPDATE camel
                SET price=?
                WHERE url=? AND type=? AND supplier=?
                """

        try:
            self.curs.execute(query, (new_price, url, type, supplier))
            self.conn.commit()

            return True

        except Exception as e:
            logger.exception("CamelModel -> update_price")

            return False

    # TODO: To change
    def check_url(self, url):
        """
        Check if a URL exists

        @param url: URL of the product
        @return: True | False
        """

        query = """
                SELECT EXISTS (
                    SELECT url
                    FROM camel
                    WHERE url=?
                )
                """

        try:
            res = self.curs.execute(query, (url,)).fetchone()
            self.conn.commit()

            return bool(res[0])

        except Exception as e:
            logger.exception("CamelModel -> check_url")

            return False

    # TODO: To change
    def count_product(self):
        """
        Count how many product there are in the db

        @return: Number of rows | False
        """

        query = """
                SELECT COUNT(*)
                FROM camel
                """

        try:
            res = self.curs.execute(query).fetchone()
            self.conn.commit()

            return int(res[0] / 12)

        except Exception as e:
            logger.exception("CamelModel -> count_product")

            return False
