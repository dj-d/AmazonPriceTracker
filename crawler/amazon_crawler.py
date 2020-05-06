import requests
from bs4 import BeautifulSoup
from models.product_model import AmazonModel
from user_agent.UserAgent import UserAgent
from services.logging_service import LoggingService

logging_service = LoggingService(name=__name__, formatter=None, datefmt=None, file_handler=None)

logger = logging_service.get_logger()

name_id = "productTitle"
availability_id = "availability"
price_id = "priceblock_ourprice"

# header = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0"}
header = {"User-Agent": UserAgent().random()}


def get_data(url):
    """
    Get title and price of the product

    @param url: URL of product on Amazon
    @return: dict(name, price) | False
    """

    try:
        data = {
            "name": None,
            "price": None
        }

        page = requests.get(url=url, headers=header)

        soup = BeautifulSoup(page.content, "html.parser")

        title = soup.find(id=name_id).get_text().strip()
        data["name"] = title

        availability = soup.find(id=availability_id).get_text().strip().replace("\n", "").split(".")

        if availability[0] != "Attualmente non disponibile":
            price = float(soup.find(id=price_id).get_text().replace("€", "").replace(",", ".").strip())
            data["price"] = price

        else:
            data["price"] = -1

        return data

    except Exception as e:
        logger.exception("amazon_crawler -> get_data")

        return False


def check_price(url):
    """
    Compare the new price taken by website with those into the Amazon table

    @param url: URL of product
    @return: dict(url, actual_price, new_price) | False
    """

    new_data = get_data(url)

    if new_data:
        actual_price = AmazonModel().get_price(url)

        if new_data["price"] != actual_price:
            data = {
                "url": url,
                "actual_price": actual_price,
                "new_price": new_data["price"]
            }

            AmazonModel().update_price(url, new_data["price"])

            return data
        else:
            return False
    else:
        return False
