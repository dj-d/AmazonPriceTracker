from models.product_model import AmazonModel, CamelModel
from services import amazon_crawler, camel_crawler


class ProductService:
    """
    Provide methods for product management
    """

    def __init__(self):
        self.amazon_model = AmazonModel()
        self.camel_model = CamelModel()

    def create(self, name, url, chat_id):
        """
        Add product

        @param name: Name of product
        @param url: URL of Amazon product
        @param chat_id:
        @return: dict
        """

        res = {
            "amazon": False,
            "camel": False
        }

        amazon_product = amazon_crawler.get_data(url)

        if amazon_product:
            res["amazon"] = self.amazon_model.create(name, amazon_product["name"], url, amazon_product["price"], chat_id)

            res["camel"] = self.create_camel_product(url)

        return res

    def create_camel_product(self, url):
        res = False

        camel_product = camel_crawler.get_info(url)

        if camel_product:
            for element in camel_product:
                for info in element["info"]:
                    res = self.camel_model.create(url, element["type"], info["supplier"], info["price"])

            return res
        else:
            return False

    def delete(self, name, chat_id):
        """
        Delete a product

        @param name: Name of the product
        @return: dict
        """

        res = {
            "amazon": False,
            "exists_in_camel": False,
            "camel": False
        }

        url = self.amazon_model.get_url_by_name(name, chat_id)

        if self.camel_model.check_url(url):
            res["exists_in_camel"] = True
            res["camel"] = self.camel_model.delete(url)

        if self.amazon_model.check_url(url, chat_id):
            res["amazon"] = self.amazon_model.delete(url, chat_id)

        return res

    def get_name(self, url, chat_id):
        """
        Get name of a product

        @param url: URL of the product
        @param chat_id:
        @return: Name of the product | False
        """

        return self.amazon_model.get_name(url, chat_id)

    def get_name_thread(self, url):
        """
        Get name of a product

        @param url: URL of the product
        @return: Name of the product | False
        """

        return self.amazon_model.get_name_thread(url)

    def get_first_name(self, chat_id):
        """
        Get name at first row of table

        @return: Name of the product | False
        """

        return self.amazon_model.get_first_name(chat_id)

    def get_url_by_name(self, name, chat_id):
        """
        Get the URL by a name

        @param name: Name of the product
        @param chat_id:
        @return: String | False
        """

        return self.amazon_model.get_url_by_name(name, chat_id)

    def get_amazon_price(self, url, chat_id):
        """
        Get price of a product by URL

        @param url: URL of the product
        @param chat_id:
        @return: Price of the product | False
        """
        return self.amazon_model.get_price(url, chat_id)

    def get_amazon_urls(self, chat_id):
        """
        Get all urls in Amazon table

        @param chat_id:
        @return: list(url) | False
        """

        return self.amazon_model.get_urls(chat_id)

    def get_camel_urls(self):
        """
        Get all urls without duplicates in Camel table

        @return: list() | False
        """

        return self.camel_model.get_urls()

    def get_amazon_info(self, chat_id):
        """
        Get name and price of a product in Amazon table

        @return: tuple(name, price) | False
        """

        res_amazon = self.amazon_model.get_info(chat_id)

        if res_amazon:
            return res_amazon

        return False

    def get_camel_info(self):
        """
        Get base information of product in Camel table

        @return: tuple(url, type, supplier, price) | False
        """

        res_camel = self.camel_model.get_info()

        if res_camel:
            return res_camel

        return False

    def update_name(self, old_name, new_name, chat_id):
        """
        Change name of a product

        @param old_name: Current name of the product
        @param new_name: New name
        @param chat_id:
        @return: True | False
        """

        return self.amazon_model.update_name(old_name, new_name, chat_id)

    def check_name(self, name, chat_id):
        """
        Check if a name exists

        @param name: Name of the product
        @param chat_id:
        @return: True | False
        """

        return self.amazon_model.check_name(name, chat_id)

    def check_amazon_url(self, url, chat_id):
        """
        Check if a URL exists in Amazon table

        @param url: URL of the product
        @param chat_id:
        @return: True | False
        """

        return self.amazon_model.check_url(url, chat_id)

    def check_camel_url(self, url):

        """
        Check if a URL exists in Camel table

        @param url: URL of the product
        @return: True | False
        """

        return self.camel_model.check_url(url)

    def count_amazon_product(self, chat_id):
        """
        Count how many product there are in Amazon table

        @return: Number of rows | False
        """
        return self.amazon_model.count_product(chat_id)

    def count_camel_product(self):
        """
        Count how many product there are in Camel table

        @return: Number of element | False
        """
        return self.camel_model.count_product()
