from bs4 import BeautifulSoup
import requests
import logging

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)




def start(update, context):
   update.message.reply_text('¡Hola! ¡Te habla el PanaMiguel 😹 y soy un bot interactivo!'
                                       '\nTe ayudaré a realizar correctamente la compra de tu boleto de vuelo'
                                       '\nElige tu opción, dando click al comando o escribiéndolo')
   update.message.reply_text('¿Qué deseas hacer?: \n\n/Tutorial - Ver instrucciones \n/Comprar - Comprar vuelo '
                             ' \n/Info - Información de aerolíneas y más \n/Cerrar - Finalizar chat\n\n')


def comprar(update, context):
    update.message.reply_text('✈Por favor, ingresa el código IATA\nSi tienes dudas ingresa 👉 https://madavan.com.mx/codigo-iata-aerolineas/ 👈')
    Origen(update, context)
    '''origen = update.message.text

    if origen in listaIata2:
        update.message.reply_text('bien')
    else:
        update.message.reply_text('mal')'''

    #update.message.reply_text('Escribe - 1 - para confirmar\nEscribe - 0 - para seleccionar otro origen')
    #dp.add_handler(MessageHandler(Filters.text, Destino))



def Origen(update, context):
    update.message.reply_text('✈Por favor, ingresa el código IATA\nSi tienes dudas ingresa 👉 https://madavan.com.mx/codigo-iata-aerolineas/ 👈')
    origen = update.message.text
    if origen in listaIata2:
            #indice = listaIata.index(origen)
            #update.message.reply_text(f'🌎El país de origen que elegiste es: {listPaises[indice]}.\n✈La aerolínea es: {listaAirlines[indice]}')
        update.message.reply_text('bien')

            #dp.add_handler(MessageHandler(Filters.text, validacion))
    else:
            update.message.reply_text('No coincide el código')
    return ConversationHandler.END
def Destino(update, context):
    origen = update.message.text.upper()
    if origen in listaIata:
        indice = listaIata.index(origen)
        update.message.reply_text(f'🌎El pasaís de origen que elegiste es: {listPaises[indice]}.\n✈La aerolínea es: {listaAirlines[indice]}')

        #dp.add_handler(MessageHandler(Filters.text, validacion))
    else:
        update.message.reply_text('error')

def validacion(update, context):
    opcion = update.message.text
    if opcion == 1:
        update.message.reply_text('Muy bien')



def datosAirlines():
    sitioCodes = 'https://madavan.com.mx/codigo-iata-aerolineas/'
    pagina = requests.get(sitioCodes)
    soup = BeautifulSoup(pagina.content, 'html.parser')
    for row in soup.findAll('table')[0].tbody.findAll('tr'):  # Validacion 2: se detiene cuando encuentra la primera tabla y todos los subcampos 'td'
        iataCodes = row.findAll('td')[0]  # busca el campo donde haya la puntuación de cada etiqueta
        airlineCodes = row.findAll('td')[1]  # busca el campo donde haya la puntuación de cada etiqueta
        paises = row.findAll('td')[4]  # busca el campo donde haya la puntuación de cada etiqueta
        listaIata.append(iataCodes.text)
        listaAirlines.append(airlineCodes.text)
        listPaises.append(paises.text)


def sumar(update,context):
    try:
        numero1 = int(context.args[0])
        numero2 = int(context.args[1])

        suma = numero1 + numero2

        update.message.reply_text("La suma es "+str(suma))

    except (ValueError):
        update.message.reply_text("por favor utilice dos numeros")


    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary


listaIata = list()
listaIata2 = ['ola','jaja']
listaAirlines = list()
listPaises = list()

datosAirlines()
updater = Updater("1275373802:AAGn8auWnyZWRjlDbO4zAD4446ThP5OSwbQ", use_context=True)

    # Get the dispatcher to register handlers
dp = updater.dispatcher

    # on different commands - answer in Telegram
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("comprar", comprar))
dp.add_handler(MessageHandler(Filters.text, Origen))


    # on noncommand i.e message - echo the message on Telegram


    # log all errors

    # Start the Bot
updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
updater.idle()

