from src.models.product_model import AmazonModel, CamelModel
from src.crawlers import amazon_crawler, camel_crawler


class ProductService:
    """
    Provide methods for product management
    """

    def __init__(self):
        self.amazon_model = AmazonModel()
        self.camel_model = CamelModel()

    def create(self, chat_id, name, url):
        """
        Add product

        @param chat_id:
        @param name: Name of product
        @param url: URL of Amazon product
        @return: dict
        """

        res = {
            "amazon": False,
            "camel": False
        }

        amazon_product = amazon_crawler.get_data(url)

        if amazon_product:
            res["amazon"] = self.amazon_model.create(chat_id, name, amazon_product["name"], url, amazon_product["price"])

            res["camel"] = self.create_camel_product(chat_id, url)

        return res

    def create_camel_product(self, chat_id, url):
        res = False

        camel_product = camel_crawler.get_info(url)

        if camel_product:
            for element in camel_product:
                for info in element["info"]:
                    res = self.camel_model.create(chat_id, url, element["type"], info["supplier"], info["price"])

            return res
        else:
            return False

    def delete(self, chat_id, name):
        """
        Delete a product

        @param chat_id:
        @param name: Name of the product
        @return: dict
        """

        res = {
            "amazon": False,
            "exists_in_camel": False,
            "camel": False
        }

        url = self.amazon_model.get_url_by_name(chat_id, name)

        if self.camel_model.check_url(chat_id, url):
            res["exists_in_camel"] = True
            res["camel"] = self.camel_model.delete(chat_id, url)

        if self.amazon_model.check_url(chat_id, url):
            res["amazon"] = self.amazon_model.delete(chat_id, url)

        return res

    def get_name(self, chat_id, url):
        """
        Get name of a product

        @param chat_id:
        @param url: URL of the product
        @return: Name of the product | False
        """

        return self.amazon_model.get_name(chat_id, url)

    def get_first_name(self, chat_id):
        """
        Get name at first row of table

        @param chat_id:
        @return: Name of the product | False
        """

        return self.amazon_model.get_first_name(chat_id)

    def get_url_by_name(self, chat_id, name):
        """
        Get the URL by a name

        @param chat_id:
        @param name: Name of the product
        @return: String | False
        """

        return self.amazon_model.get_url_by_name(chat_id, name)

    def get_amazon_price(self, chat_id, url):
        """
        Get price of a product by URL

        @param chat_id:
        @param url: URL of the product
        @return: Price of the product | False
        """

        return self.amazon_model.get_price(chat_id, url)

    def get_amazon_urls(self, chat_id):
        """
        Get all urls in Amazon table

        @param chat_id:
        @return: list(url) | False
        """

        return self.amazon_model.get_urls(chat_id)

    def get_camel_urls(self, chat_id):
        """
        Get all urls without duplicates in Camel table

        @param chat_id:
        @return: list() | False
        """

        return self.camel_model.get_urls(chat_id)

    def get_amazon_info(self, chat_id):
        """
        Get name and price of a product in Amazon table

        @param chat_id:
        @return: tuple(name, price) | False
        """

        res_amazon = self.amazon_model.get_info(chat_id)

        if res_amazon:
            return res_amazon

        return False

    def get_camel_info(self, chat_id):
        """
        Get base information of product in Camel table

        @param chat_id:
        @return: tuple(url, type, supplier, price) | False
        """

        res_camel = self.camel_model.get_info(chat_id)

        if res_camel:
            return res_camel

        return False

    def update_name(self, chat_id, old_name, new_name):
        """
        Change name of a product

        @param chat_id:
        @param old_name: Current name of the product
        @param new_name: New name
        @return: True | False
        """

        return self.amazon_model.update_name(chat_id, old_name, new_name)

    def check_name(self, chat_id, name):
        """
        Check if a name exists

        @param chat_id:
        @param name: Name of the product
        @return: True | False
        """

        return self.amazon_model.check_name(chat_id, name)

    def check_amazon_url(self, chat_id, url):
        """
        Check if a URL exists in Amazon table

        @param chat_id:
        @param url: URL of the product
        @return: True | False
        """

        return self.amazon_model.check_url(chat_id, url)

    def check_camel_url(self, chat_id, url):

        """
        Check if a URL exists in Camel table

        @param chat_id:
        @param url: URL of the product
        @return: True | False
        """

        return self.camel_model.check_url(chat_id, url)

    def count_amazon_product(self, chat_id):
        """
        Count how many product there are in Amazon table

        @return: Number of rows | False
        """

        return self.amazon_model.count_product(chat_id)

    def count_camel_product(self, chat_id):
        """
        Count how many product there are in Camel table

        @return: Number of element | False
        """

        return self.camel_model.count_product(chat_id)
