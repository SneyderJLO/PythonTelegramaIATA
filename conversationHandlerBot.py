from bs4 import BeautifulSoup
import requests

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
from telegram import ReplyKeyboardMarkup
CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [['Origen', 'Destino', 'Fechas'],
                  ['Pasajeros', 'Confirmar compra', 'Restaurar compra'],
                  ['Done']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

def start(update, context):
   update.message.reply_text('¡Hola! ¡Te habla el PanaMiguel 😹 y soy un bot interactivo!'
                                       '\nTe ayudaré a realizar correctamente la compra de tu boleto de vuelo.'
                                       '\nElige tu opción, dando click al comando o escribiéndolo', reply_markup=markup)
   return CHOOSING


def done(update, context):
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text("I learned these facts about you:"
                              "{}"
                              "Until next time!".format(facts_to_str(user_data)))

    user_data.clear()
    return ConversationHandler.END


def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])

def regular_choice(update, context):
    text = update.message.text
    context.user_data['choice'] = text
    update.message.reply_text(
        'Seleccionaste {}.\nPor favor, ingresa el dato.'.format(text.lower()))
    return TYPING_REPLY


def custom_choice(update, context):
    update.message.reply_text('Alright, please send me the category first, '
                              'for example "Most impressive skill"')

    return TYPING_CHOICE


def received_information(update, context):
    flag = False
    user_data = context.user_data
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']
    if user_data['Origen']:
        if user_data['Origen'] == 'ola':
            update.message.reply_text('Correcto')
            update.message.reply_text("¡Muy bien! Estos son tus datos:"
                                      "{}Puedes cambiar de dato cuando quieras, simplemente entra al botón que quieras.".format(
                facts_to_str(user_data)),
                                      reply_markup=markup)
        else:
            update.message.reply_text('Incorrecto. Ingresa de nuevo el dato seleccionado el botón Origen',
                                      reply_markup=markup)

    print(user_data['Origen'])
    print(type(user_data))
    print(text)
    return CHOOSING


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1275373802:AAGn8auWnyZWRjlDbO4zAD4446ThP5OSwbQ", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSING: [MessageHandler(Filters.regex('^(Origen|Destino|Fechas|Pasajeros|Confirmar Comprar|Restaurar compra)$'),
                                      regular_choice),
                       MessageHandler(Filters.regex('^Something else...$'),
                                      custom_choice)
                       ],

            TYPING_CHOICE: [
                MessageHandler(Filters.text & ~(Filters.command | Filters.regex('^Done$')),
                               regular_choice)],

            TYPING_REPLY: [
                MessageHandler(Filters.text & ~(Filters.command | Filters.regex('^Done$')),
                               received_information)],
        },

        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)]
    )

    dp.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()



