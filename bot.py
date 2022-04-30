import logging
import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import apiAccess as flightApi
from data import DAL
import secrets

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
params_for_flight_search = []


def start(update, context):
    params_for_flight_search.clear()
    update.message.reply_text("Choose the airport you want to depart from:",
                              reply_markup=main_menu_keyboard())


def main_menu(update, context):
    params_for_flight_search.clear()
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="Choose the airport you want to depart from:",
        reply_markup=main_menu_keyboard())
    print(params_for_flight_search)


def first_menu(update, context):
    query = update.callback_query
    params_for_flight_search.append(query.data)
    query.answer()
    query.edit_message_text(
        text="you chose to depart from " + params_for_flight_search[0] + "\n where would you like to go",
        reply_markup=first_menu_keyboard())
    print(params_for_flight_search)


def second_menu(update, context):
    query = update.callback_query
    params_for_flight_search.append(query.data)
    query.answer()
    query.edit_message_text(
        text="you chose to depart from " + params_for_flight_search[0] + " to " + params_for_flight_search[
            1] + "\n when would you like to depart",
        reply_markup=second_menu_keyboard())
    print(params_for_flight_search)


def third_menu(update, context):
    query = update.callback_query
    params_for_flight_search.append(query.data)
    query.answer()
    flight_info = flightApi.Get_flight_info(params_for_flight_search)
    print(flight_info)
    if flight_info is None:
        query.edit_message_text(
            text="im very  sorry but there is no flights who fits to your preferences ",
            reply_markup=main_menu_keyboard())
        params_for_flight_search.clear()
        return
    query.edit_message_text(
        text="You chose to depart from " + params_for_flight_search[0]
             + " to " + params_for_flight_search[1]
             + " at " + params_for_flight_search[2]
             + "\n\nThis are the best results for you:\n"
             + flight_info,
        reply_markup=main_menu_keyboard())

    DAL.Better_new_same(flightApi.Get_flight_info_dic(params_for_flight_search))
    print(params_for_flight_search)
    params_for_flight_search.clear()


##### returns an arry of days of the week formated to dates ####
def DaysOfTheWeek():
    d_zero = datetime.datetime.today()
    d_one = datetime.datetime.today() + datetime.timedelta(days=1)
    d_two = datetime.datetime.today() + datetime.timedelta(days=2)
    d_three = datetime.datetime.today() + datetime.timedelta(days=3)
    d_four = datetime.datetime.today() + datetime.timedelta(days=4)
    d_five = datetime.datetime.today() + datetime.timedelta(days=5)
    d_six = datetime.datetime.today() + datetime.timedelta(days=6)
    array_of_days = []
    array_of_days.extend([d_zero, d_one, d_two, d_three, d_four, d_five, d_six])
    return array_of_days


############################ Keyboards #########################################
def main_menu_keyboard():
    keyboard = [[InlineKeyboardButton("TLV Israel", callback_data='TLV-sky'),
                 InlineKeyboardButton("ETM ramon international", callback_data='ETM-sky')]]
    return InlineKeyboardMarkup(keyboard)


def first_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Berlin', callback_data='BER-sky')],
                [InlineKeyboardButton('Budapest', callback_data='BUD-sky')],
                [InlineKeyboardButton('Athens', callback_data='ATH-sky')],
                [InlineKeyboardButton('Paris', callback_data='CDG-sky')],
                [InlineKeyboardButton('Madrid', callback_data='MAD-sky')],
                [InlineKeyboardButton('Lisbon', callback_data='LIS-sky')],
                [InlineKeyboardButton('Zurich', callback_data='ZRH-sky')],
                [InlineKeyboardButton('Main menu', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)


def second_menu_keyboard():
    days = DaysOfTheWeek()
    keyboard = []
    for i in range(7):
        keyboard.append([InlineKeyboardButton(days[i].strftime('%Y-%m-%d'),
                                              callback_data=days[i].strftime('%Y-%m-%d'))])
    keyboard.append([InlineKeyboardButton('Main menu', callback_data='main')])
    return InlineKeyboardMarkup(keyboard)


def main() -> None:
    updater = Updater(secrets.API_KEY)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
    updater.dispatcher.add_handler(CallbackQueryHandler(first_menu, pattern='TLV-sky'))
    updater.dispatcher.add_handler(CallbackQueryHandler(first_menu, pattern='ETM-sky'))
    updater.dispatcher.add_handler(CallbackQueryHandler(second_menu, pattern='BER-sky'))
    updater.dispatcher.add_handler(CallbackQueryHandler(second_menu, pattern='BUD-sky'))
    updater.dispatcher.add_handler(CallbackQueryHandler(second_menu, pattern='ATH-sky'))
    updater.dispatcher.add_handler(CallbackQueryHandler(second_menu, pattern='CDG-sky'))
    updater.dispatcher.add_handler(CallbackQueryHandler(second_menu, pattern='MAD-sky'))
    updater.dispatcher.add_handler(CallbackQueryHandler(second_menu, pattern='LIS-sky'))
    updater.dispatcher.add_handler(CallbackQueryHandler(second_menu, pattern='ZRH-sky'))
    days = DaysOfTheWeek()
    for i in range(7):
        updater.dispatcher.add_handler(CallbackQueryHandler(third_menu, pattern=days[i].strftime('%Y-%m-%d')))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
