import os
import signal

from bs4 import BeautifulSoup
import requests
import logging

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)




def start(update, context):
   update.message.reply_text('¡Hola! ¡Te habla el PanaMiguel 😹 y soy un bot interactivo!'
                                       '\nTe ayudaré a realizar correctamente la compra de tu boleto de vuelo.'
                                       '\nElige tu opción, dando click al comando o escribiéndolo')
   update.message.reply_text('¿Qué deseas hacer?: \n\n/Tutorial - Ver instrucciones \n/Comprar - Comprar vuelo '
                             ' \n/Info - Información de aerolíneas y más \n/Cerrar - Finalizar chat\n\n')



def comprar(update, context):
    update.message.reply_text('✈Si no conoces el código, puedes visitar \n👉 https://madavan.com.mx/codigo-iata-aerolineas/ 👈')
    update.message.reply_text('/Continuar')
    #dp.add_handler(CommandHandler('Origen', Origen))
    dp.add_handler(CommandHandler('Continuar', Origen))
    #dp.add_handler(CommandHandler('Proceder', Destino))
    #update.message.reply_text('Escribe - 1 - para confirmar\nEscribe - 0 - para seleccionar otro origen')



def Origen(update, context):

    update.message.reply_text('✈Por favor, ingresa el código iata de tu origen.')
    dp.add_handler(MessageHandler(Filters.update.message, listener, pass_user_data=True))

    os.kill(os.getpid(), signal.SIGINT)
    return ConversationHandler.END


def listener(update, context):
    context.user_data ['listener'] = update.message.text
    mensaje = update.message.text.upper()
    if mensaje in listaIata:
        indice = listaIata.index(mensaje)
        listaIata.pop(indice)


        update.message.reply_text(f'🌎El pasaís de origen que elegiste es: {listPaises[indice]}.\n✈La aerolínea es: {listaAirlines[indice]}')
        if len(listaSeleccion) <= 2:
            listaSeleccion.append(mensaje)
        update.message.reply_text('/Proceder')
    else:
        update.message.reply_text('❌ Error - El código no existe o ya lo escogiste.\n🔁 Intenta de nuevo')

    user_data.clear()
    return ConversationHandler.END

def Destino(update, context):
    update.message.reply_text('✈Por favor, ingresa el código iata para su destino.')
    dp.add_handler(MessageHandler(Filters.text, listener))

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
listaSeleccion = list()
listaIata = list()
listaAirlines = list()
listPaises = list()
datosAirlines()
updater = Updater("1275373802:AAGn8auWnyZWRjlDbO4zAD4446ThP5OSwbQ", use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("comprar", comprar))
updater.start_polling()
updater.idle()

