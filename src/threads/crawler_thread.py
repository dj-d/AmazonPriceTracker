from time import sleep
from threading import Thread

from . import constant

from ..services.logging_service import LoggingService
from ..services.product_service import ProductService

logging_service = LoggingService(name=__name__, formatter=None, datefmt=None, file_handler=None)

logger = logging_service.get_logger()


class CrawlerThread(Thread):
    def __init__(self, products, service, time, chat_id):
        Thread.__init__(self)

        self.products = products
        self.service = service
        self.time = time
        self.changes = []
        self.chat_id = chat_id

    def run(self):
        for url in self.products:
            name = ProductService().get_name(self.chat_id, url[0])

            # service_name = str(self.service).split("/")[8].replace(".py'>", "")   # For Command Line
            service_name = str(self.service).split("/")[3].replace(".py'>", "")     # For Docker

            logger.info(service_name + " -> " + name + "...")

            new_info = self.service.check_price(self.chat_id, url[0])

            if new_info:
                if service_name == "amazon_crawler":
                    if new_info["actual_price"] < new_info["new_price"]:
                        self.changes.append(name + " has risen from €" + str(new_info["actual_price"]) + constant.TO_EURO + str(new_info["new_price"]))
                    else:
                        self.changes.append(name + " has come down from €" + str(new_info["actual_price"]) + constant.TO_EURO + str(new_info["new_price"]))

                elif service_name == "camel_crawler":
                    i = 0
                    while i < len(new_info):
                        price_type = new_info[i]["type"]
                        supplier = new_info[i]["supplier"]

                        if float(new_info[i]["actual_price"]) < float(new_info[i]["new_price"]):
                            self.changes.append(name + ", sold by: " + supplier + " (" + price_type + ")" + " has risen from €" + str(new_info[i]["actual_price"]) + constant.TO_EURO + str(new_info[i]["new_price"]))

                        else:
                            self.changes.append(name + ", sold by: " + supplier + " (" + price_type + ")" + " has come down from €" + str(new_info[i]["actual_price"]) + constant.TO_EURO + str(new_info[i]["new_price"]))

                        i += 1

            sleep(self.time)

    def get_changes(self):
        return self.changes
