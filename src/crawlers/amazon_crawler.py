import requests
from bs4 import BeautifulSoup
from src.models.product_model import AmazonModel
from src.user_agent.UserAgent import UserAgent
from src.services.logging_service import LoggingService

from . import constant

logging_service = LoggingService(name=__name__, formatter=None, datefmt=None, file_handler=None)

logger = logging_service.get_logger()

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

        title = soup.find(id=constant.NAME_ID).get_text().strip()
        data["name"] = title

        availability = soup.find(id=constant.AVAILABILITY_ID).get_text().strip().replace("\n", "").split(".")

        if availability[0] != "Attualmente non disponibile":
            raw_price = soup.find(id=constant.OUR_PRICE_ID)

            if raw_price is None:
                raw_price = soup.find(id=constant.DEAL_PRICE_ID)

            if raw_price is not None:
                data["price"] = float(raw_price.get_text().replace("€", "").replace(",", ".").strip())
            else:
                data["price"] = -1
                logger.error("amazon_crawler -> Price not find")

        else:
            data["price"] = -1

        return data

    except Exception:
        logger.exception("amazon_crawler -> get_data")

        return False


def check_price(chat_id, url):
    """
    Compare the new price taken by website with those into the Amazon table

    @param chat_id:
    @param url: URL of product
    @return: dict(url, actual_price, new_price) | False
    """

    new_data = get_data(url)

    if new_data:
        actual_price = AmazonModel().get_price(chat_id, url)

        if new_data["price"] != actual_price:
            data = {
                "url": url,
                "actual_price": actual_price,
                "new_price": new_data["price"]
            }

            AmazonModel().update_price(chat_id, url, new_data["price"])

            return data
        else:
            return False
    else:
        return False
