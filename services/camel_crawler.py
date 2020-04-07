import requests
from bs4 import BeautifulSoup
from UserAgent import UserAgent
from models.product_model import CamelModel
from services.logging_service import LoggingService

logging_service = LoggingService(name=__name__, formatter=None, datefmt=None, file_handler=None)

logger = logging_service.get_logger()

header = {"User-Agent": UserAgent().random()}


def get_url(url):
    """
    Make URL to search product data

    @param url: URL of Amazon product
    @return: URL of product
    """

    head = "https://it.camelcamelcamel.com/search?sq="

    return head + url


def get_data(url):
    """
    Get the vendors table

    @param url: URL of Amazon product
    @return: list() | False
    """

    try:
        product_url = get_url(url)

        page = requests.get(url=product_url, headers=header)
        soup = BeautifulSoup(page.content, "html.parser")

        data = soup.find(class_="row column hide-for-large")

        if data is not None:
            data = data.get_text().split("\n")
            data = list(filter(None, data))

            return data
        else:
            return False  # Quando non ci sono dati ritarna False

    except Exception as e:
        logger.exception("camel_crawler -> get_data")

        return False


def format_website_data(raw_data):
    """
    Format data takes on website in a dictionary

    @param raw_data: list of string
    @return: dict()
    """

    for i in range(2):
        raw_data.pop(0)

    new_data = list()
    i = 0
    index = -1
    while i < len(raw_data):
        if ((i % 3) == 0) and ((i % 12) == 0):
            index += 1

            data = {
                "type": raw_data[i + 1],
                "info": []
            }

            new_data.append(data)

        elif ((i % 3) == 0) and (not ((i % 12) == 0)):
            if raw_data[i + 1] == "Not in stock":
                price = -1
            else:
                price = raw_data[i + 1].replace(",", ".").replace("€", "")

            info = {
                "supplier": raw_data[i].replace("Prezzo ", "").strip().capitalize(),
                "price": float(price)
            }

            new_data[index]["info"].append(info)

        i += 3

    return new_data


def get_info(url):
    """
    Get sales information

    @param url: URL of Amazon product
    @return: dict() | False
    """

    raw_data = get_data(url)

    if raw_data:
        return format_website_data(raw_data)

    else:
        return False


def format_db_data(raw_data):
    """
    Format data takes into the Camel table in a dictionary

    @param raw_data: list
    @return: dict
    """

    new_data = list()
    i = 0
    index = -1
    while i < len(raw_data):
        if (i % 3) == 0:
            index += 1
            data = {
                "type": raw_data[i][0],
                "info": [{
                    "supplier": raw_data[i][1],
                    "price": raw_data[i][2]
                }]
            }

            new_data.append(data)
        else:
            info = {
                "supplier": raw_data[i][1],
                "price": raw_data[i][2]
            }

            new_data[index]["info"].append(info)

        i += 1

    return new_data


def check_price(url):
    """
    Compare the new prices taken by website with those into the Camel table

    @param url: URL of Amazon product
    @return: list(dict) | False
    """

    new_info = []

    new_data = get_info(url)

    raw_actual_data = CamelModel().get_price_info(url)

    if new_data and raw_actual_data:
        actual_data = format_db_data(raw_actual_data)

        i = 0
        while i < len(new_data):
            j = 0
            while j < len(new_data[i]["info"]):
                if new_data[i]["info"][j]["price"] != actual_data[i]["info"][j]["price"]:
                    data = {
                        "url": url,
                        "type": actual_data[i]["type"],
                        "supplier": actual_data[i]["info"][j]["supplier"],
                        "actual_price": actual_data[i]["info"][j]["price"],
                        "new_price": new_data[i]["info"][j]["price"]
                    }

                    CamelModel().update_price(url, actual_data[i]["type"], actual_data[i]["info"][j]["supplier"], new_data[i]["info"][j]["price"])

                    new_info.append(data)

                j += 1

            i += 1

        return new_info
    else:
        return False
