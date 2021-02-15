from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler)
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from emoji import emojize
import validators
import json

from src.services.logging_service import LoggingService
from src.services.product_service import ProductService
from src.services.crawler_thread import CrawlerThread

from src.models.product_model import Schema

from src.crawlers import amazon_crawler, camel_crawler


logging_service = LoggingService(name=__name__, formatter=None, datefmt=None, file_handler=None)

logger = logging_service.get_logger()

with open('credential.json') as json_file:
    data = json.load(json_file)
    TOKEN = data["TOKEN"]

CHOOSING, ADD_SECOND_STEP, ADD_THIRD_STEP, REMOVE_SECOND_STEP, CHANGE_SECOND_STEP, CHANGE_THIRD_STEP, GET_URL_SECOND_STEP = range(7)

reply_keyboard = [
    [
        emojize(":clipboard: Product list", use_aliases=True),
        emojize(" :heavy_plus_sign: Add", use_aliases=True),
        emojize(":page_with_curl: Get url", use_aliases=True)
    ],
    [
        emojize(":clipboard: More info", use_aliases=True),
        emojize(':wastebasket: Remove', use_aliases=True),
        emojize(":twisted_rightwards_arrows: Change name", use_aliases=True)
    ],
    [
        emojize(":information_source: Help", use_aliases=True)
    ]
]

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)

user_id = None

product_details = {
    "name": None,
    "url": None
}

product_name = {
    "old_name": None,
    "new_name": None
}


def check_url(url):
    """
    Check if an URL is valid

    @param url: URL to check
    @return: True | False
    """

    if validators.url(url):
        return True

    return False


def start_conversation(update, context):
    global user_id

    user_id = update.message.from_user['id']
    username = update.message.from_user['username']

    msg = "Hi @" + username + ",\n" \
          "This bot was created to track the price of products taken on Amazon.\n" \
          "It is not yet in final version, but for those who want to contribute the link to the repository is: " \
                              "https://github.com/dj-d/AmazonPriceTracker\n"

    update.message.reply_text(
        msg,
        reply_markup=markup
    )

    update.message.reply_text(
        "Choose from the following options:",
        reply_markup=markup
    )

    return CHOOSING


def amazon_product_list(update, context):
    products = ProductService().get_amazon_info(
        chat_id=update.message.from_user['id']
    )

    info = "Amazon products: \n"

    if not products:
        info += "   - Any products"
    else:
        for element in products:
            if element[1] != -1:
                info += "   - " + str(element[0]) + ", €" + str(element[1]) + "\n"
            else:
                info += "   - " + str(element[0]) + ", Not in stock" + "\n"

    update.message.reply_text(info)

    return CHOOSING


# TODO: Make for only one product
def camel_product_list(update, context):
    products = ProductService().get_camel_info(
        chat_id=update.message.from_user['id']
    )

    info = "Camel products: \n"

    if not products:
        info += "   - Any products"
    else:
        i = 0
        while i < len(products):
            if (i % 12) == 0:
                info += " - " + ProductService().get_name(
                    chat_id=update.message.from_user['id'],
                    url=products[i][0]
                ) + ":\n"  # name

            if (i % 3) == 0:
                info += "     - " + products[i][1] + ":\n"  # type

            raw_price = products[i][3]

            if raw_price == -1:  # supplier + price
                info += "         - " + products[i][2] + ", Not in stock" + "\n"
            else:
                info += "         - " + products[i][2] + ", €" + str(raw_price) + "\n"

            i += 1

    update.message.reply_text(info)

    return CHOOSING


def add_set_name(update, context):
    update.message.reply_text(
        "Enter product name: ",
        reply_markup=markup
    )

    return ADD_SECOND_STEP


def add_set_url(update, context):
    global product_details

    product_details["name"] = update.message.text

    if not ProductService().check_name(chat_id=update.message.from_user['id'], name=product_details["name"]):
        update.message.reply_text(
            "Enter amazon product URL: ",
            reply_markup=markup
        )

        return ADD_THIRD_STEP

    elif product_details["name"] == "/stop":
        return stop_conversation(
            update=update,
            context=context
        )

    else:
        update.message.reply_text(
            "Name already exists",
            reply_markup=markup
        )

        add_set_name(
            update=update,
            context=context
        )


def add_update_db(update, context):
    global product_details

    product_details["url"] = update.message.text

    if check_url(product_details["url"]) and \
            (not ProductService().check_amazon_url(chat_id=update.message.from_user['id'], url=product_details["url"])):
        res = ProductService().create(
            chat_id=update.message.from_user['id'],
            name=product_details["name"],
            url=product_details["url"]
        )

        actual_price = str(ProductService().get_amazon_price(
            chat_id=update.message.from_user['id'],
            url=product_details["url"])
        )

        if res["amazon"] and res["camel"]:
            update.message.reply_text(
                "Done, now, the current price is €" + actual_price,
                reply_markup=markup
            )

        elif res["amazon"] and not res["camel"]:
            update.message.reply_text(
                "Added only in the Amazon table, now, the current price is €" + actual_price,
                reply_markup=markup
            )

        else:
            update.message.reply_text(
                "Error",
                reply_markup=markup
            )

        return CHOOSING

    elif product_details["url"] == "/stop":
        return stop_conversation(
            update=update,
            context=context
        )

    else:
        update.message.reply_text(
            "Not valid URL",
            reply_markup=markup
        )

        add_set_url(
            update=update,
            context=context
        )


def remove_set_name(update, context):
    update.message.reply_text(
        "Enter the name of the product to be deleted: ",
        reply_markup=markup
    )

    return REMOVE_SECOND_STEP


def remove_update_db(update, context):
    name = update.message.text

    if ProductService().check_name(chat_id=update.message.from_user['id'], name=name):
        res = ProductService().delete(
            chat_id=update.message.from_user['id'],
            name=name
        )

        if (res["amazon"] and res["exists_in_camel"] and res["camel"]) or (res["amazon"] and not res["exists_in_camel"]):
            update.message.reply_text(
                "Done",
                reply_markup=markup
            )

        elif res["amazon"] and res["exists_in_camel"] and not res["camel"]:
            update.message.reply_text(
                "Removed only in Amazon table for unknown reasons",
                reply_markup=markup
            )

        else:
            update.message.reply_text(
                "Error",
                reply_markup=markup
            )

        return CHOOSING

    elif name == "/stop":
        return stop_conversation(
            update=update,
            context=context
        )

    else:
        update.message.reply_text(
            "Not valid name",
            reply_markup=markup
        )

        remove_set_name(
            update=update,
            context=context
        )
        

def change_set_old_name(update, context):
    if ProductService().count_amazon_product(chat_id=update.message.from_user['id']) != 0:
        update.message.reply_text(
            "Enter current name of the product: ",
            reply_keyboard=markup
        )

        return CHANGE_SECOND_STEP
    else:
        update.message.reply_text(
            "There are no products to change its name",
            reply_keyboard=markup
        )

        return CHOOSING


def change_set_new_name(update, context):
    global product_name
    
    product_name["old_name"] = update.message.text

    if product_name["old_name"] == "/stop":
        return stop_conversation(
            update=update,
            context=context
        )
    
    elif ProductService().check_name(chat_id=update.message.from_user['id'], name=product_name["old_name"]):
        update.message.reply_text(
            "Enter new name: ",
            reply_keyboard=markup
        )
        
        return CHANGE_THIRD_STEP

    else:
        update.message.reply_text(
            "Name not exists",
            reply_markup=markup
        )

        change_set_old_name(
            update=update,
            context=context
        )


def change_update_db(update, context):
    global product_name

    product_name["new_name"] = update.message.text

    if product_name["new_name"] == "/stop":
        return stop_conversation(
            update=update,
            context=context
        )

    elif not ProductService().check_name(chat_id=update.message.from_user['id'], name=product_name["new_name"]):
        res = ProductService().update_name(
            chat_id=update.message.from_user['id'],
            old_name=product_name["old_name"],
            new_name=product_name["new_name"]
        )

        if res:
            update.message.reply_text(
                "Done",
                reply_markup=markup
            )
        else:
            update.message.reply_text(
                "Error",
                eply_markup=markup
            )

        return CHOOSING

    else:
        update.message.reply_text(
            "Name already exists",
            reply_markup=markup
        )

        change_set_new_name(
            update=update,
            context=context
        )


def get_url_set_name(update, context):
    if ProductService().count_amazon_product(chat_id=update.message.from_user['id']) > 1:
        update.message.reply_text(
            "Enter the name of the product that you want get url: ",
            reply_markup=markup
        )

        return GET_URL_SECOND_STEP

    elif ProductService().count_amazon_product(chat_id=update.message.from_user['id']) == 1:
        name = ProductService().get_first_name(
            chat_id=update.message.from_user['id']
        )

        if ProductService().check_name(chat_id=update.message.from_user['id'], name=name) and name:
            url = ProductService().get_url_by_name(
                chat_id=update.message.from_user['id'],
                name=name
            )

            update.message.reply_text(
                url,
                reply_markup=markup
            )
        else:
            update.message.reply_text(
                "Error",
                reply_markup=markup
            )

    else:
        update.message.reply_text(
            "There are no products to look for in the url",
            reply_keyboard=markup
        )

    return CHOOSING


def get_url_search_db(update, context):
    name = update.message.text

    if ProductService().check_name(chat_id=update.message.from_user['id'], name=name):
        res = ProductService().get_url_by_name(
            chat_id=update.message.from_user['id'],
            name=name
        )

        if res:
            update.message.reply_text(
                res,
                reply_markup=markup
            )
        else:
            update.message.reply_text(
                "Error",
                reply_markup=markup
            )

        return CHOOSING

    elif name == "/stop":
        return stop_conversation(
            update=update,
            context=context
        )

    else:
        update.message.reply_text(
            "Not valid name",
            reply_markup=markup
        )

        get_url_set_name(
            update=update,
            context=context
        )


def command_list(update, context):
    info = "Command List:\n"

    info += "   - /start: Start or restart the bot \n" \
            "   - /stop: Stop any action \n" \
            "   - /product_list: The list of all products and their prices \n" \
            "   - /add: Add a new product \n" \
            "   - /remove: Remove a product \n" \
            "   - /more_info: More information about the price of a product \n" \
            "   - /get_url: Get the URL of a product \n" \
            "   - /change_name: Changing the name of a product \n" \
            "   - /help: View this message \n"

    info += "\nP.S. When doing any operation, whether it's starting an action or entering text, " \
            "before doing anything else wait for the bot to respond to your last sent message."

    update.message.reply_text(
        info,
        reply_markup=markup
    )

    return CHOOSING


def check_price(context):
    logger.info("Amazon price check in progress...")

    amazon_info = "Updates: \n"

    amazon_product = ProductService().get_amazon_urls(chat_id=user_id)
    camel_product = ProductService().get_camel_urls(chat_id=user_id)

    amazon_thread = CrawlerThread(
        products=amazon_product,
        service=amazon_crawler,
        time=900,
        chat_id=user_id
    )
    amazon_thread.start()

    while amazon_thread.is_alive():
        logger.info("Camel price check in progress...")

        camel_info = "Update: \n"

        camel_thread = CrawlerThread(
            products=camel_product,
            service=camel_crawler,
            time=30,
            chat_id=user_id
        )
        camel_thread.start()

        camel_thread.join()

        if len(camel_thread.get_changes()) != 0:
            for element in camel_thread.get_changes():
                camel_info += "   - " + element + "\n"

            context.bot.send_message(
                chat_id=user_id,
                text=camel_info
            )

        logger.info("Camel finish\n")

    amazon_thread.join()

    if len(amazon_thread.get_changes()) != 0:
        for element in amazon_thread.get_changes():
            amazon_info += "   - " + element + "\n"

        context.bot.send_message(
            chat_id=user_id,
            text=amazon_info
        )

    logger.info("Amazon finish\n")


def stop_conversation(update, context):
    update.message.reply_text(
        "Stop action",
        reply_markup=markup
    )

    return CHOOSING


def error(update, context):
    logger.error(
        'Update "%s" caused error "%s"',
        update,
        context.error
    )


def cancel(update, context):
    user = update.message.from_user

    logger.info(
        "User %s canceled the conversation.",
        user.first_name
    )

    update.message.reply_text(
        'Bye! I hope we can talk again some day.',
        reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    job = updater.job_queue

    con_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start_conversation)
        ],

        states={
            CHOOSING: [
                MessageHandler(Filters.regex('Product list'), amazon_product_list),
                MessageHandler(Filters.regex('Add'), add_set_name),
                MessageHandler(Filters.regex('Remove'), remove_set_name),
                MessageHandler(Filters.regex('More info'), camel_product_list),
                MessageHandler(Filters.regex('Get url'), get_url_set_name),
                MessageHandler(Filters.regex('Change name'), change_set_old_name),
                MessageHandler(Filters.regex('Help'), command_list),

                # TODO: To improve
                MessageHandler(Filters.regex('product_list'), amazon_product_list),
                MessageHandler(Filters.regex('add'), add_set_name),
                MessageHandler(Filters.regex('remove'), remove_set_name),
                MessageHandler(Filters.regex('more_info'), camel_product_list),
                MessageHandler(Filters.regex('get_url'), get_url_set_name),
                MessageHandler(Filters.regex('change_name'), change_set_old_name),
                MessageHandler(Filters.regex('help'), command_list)
            ],

            ADD_SECOND_STEP: [
                MessageHandler(Filters.text, add_set_url)
            ],

            ADD_THIRD_STEP: [
                MessageHandler(Filters.text, add_update_db)
            ],

            REMOVE_SECOND_STEP: [
                MessageHandler(Filters.text, remove_update_db)
            ],
            
            CHANGE_SECOND_STEP: [
                MessageHandler(Filters.text, change_set_new_name)
            ],

            CHANGE_THIRD_STEP: [
                MessageHandler(Filters.text, change_update_db)
            ],

            GET_URL_SECOND_STEP: [
                MessageHandler(Filters.text, get_url_search_db)
            ]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(con_handler)
    dp.add_error_handler(error)

    job.run_repeating(
        callback=check_price,
        interval=((ProductService().count_amazon_product(user_id) + 1) * 900)
    )

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    Schema()
    main()
