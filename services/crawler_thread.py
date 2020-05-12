from services.logging_service import LoggingService
from services.product_service import ProductService
from threading import Thread
from time import sleep
import json

logging_service = LoggingService(name=__name__, formatter=None, datefmt=None, file_handler=None)

logger = logging_service.get_logger()


class CrawlerThread(Thread):
    def __init__(self, products, service, time):
        Thread.__init__(self)
        self.products = products
        self.service = service
        self.time = time
        self.changes = []

    def run(self):
        for url in self.products:
            name = ProductService().get_name(url[0])
            # service_name = str(self.service).split("/")[8].replace(".py'>", "")
            service_name = str(self.service).split("/")[3].replace(".py'>", "")  # For Docker

            logger.info(service_name + " -> " + name + "...")

            new_info = self.service.check_price(url[0])

            if new_info:
                if service_name == "amazon_crawler":
                    if new_info["actual_price"] < new_info["new_price"]:
                        self.changes.append(name + " has risen from €" + str(new_info["actual_price"]) + " to €" + str(new_info["new_price"]))
                    else:
                        self.changes.append(name + " has come down from €" + str(new_info["actual_price"]) + " to €" + str(new_info["new_price"]))

                elif service_name == "camel_crawler":
                    i = 0
                    while i < len(new_info):
                        type = new_info[i]["type"]
                        supplier = new_info[i]["supplier"]

                        if float(new_info[i]["actual_price"]) < float(new_info[i]["new_price"]):
                            if float(new_info[i]["new_price"]) is not -1:
                                self.changes.append(name + ", sold by: " + supplier + " (" + type + ")" + " has risen from €" + str(new_info[i]["actual_price"]) + " to €" + str(new_info[i]["new_price"]))
                            else:
                                self.changes.append(name + ", sold by: " + supplier + " (" + type + ")" + " has risen from €" + str(new_info[i]["actual_price"]) + " to Not in stock")
                        else:
                            if float(new_info[i]["actual_price"]) is not -1:
                                self.changes.append(name + ", sold by: " + supplier + " (" + type + ")" + " has come down from €" + str(new_info[i]["actual_price"]) + " to €" + str(new_info[i]["new_price"]))
                            else:
                                self.changes.append(name + ", sold by: " + supplier + " (" + type + ")" + " has come down from Not in stock to €" + str(new_info[i]["new_price"]))

                        i += 1

                self.changes.append("URL: " + self.get_referral_url(url[0]))

            sleep(self.time)

    def get_changes(self):
        return self.changes

    @staticmethod
    def get_referral_url(url):
        with open('credential.json') as json_file:
            data = json.load(json_file)

        tag = "?tag="
        referral_id = data["amazon"]["referral_id"]

        return url[:44] + tag + referral_id
