import threading as th
import telebot
from telebot import types
import time
import json
import numpy as np

from bs4 import BeautifulSoup
import requests
import telegram
from telegram.ext import *
from telegram.ext import CommandHandler



def Updates():
    updates = list()
    while True:
        if len(updates) > 0:
            break

        else:
            updates = bot.get_updates()



def datosAirlines():
    sitioCodes = 'https://madavan.com.mx/codigo-iata-aerolineas/'
    pagina = requests.get(sitioCodes)
    soup = BeautifulSoup(pagina.content, 'html.parser')
    for row in soup.findAll('table')[0].tbody.findAll('tr'):  # Validacion 2: se detiene cuando encuentra la primera tabla y todos los subcampos 'td'
        iataCodes = row.findAll('td')[0]  # busca el campo donde haya la puntuación de cada etiqueta
        airlineCodes = row.findAll('td')[1]  # busca el campo donde haya la puntuación de cada etiqueta
        paises = row.findAll('td')[4]  # busca el campo donde haya la puntuación de cada etiqueta
        listaIata.append('/'+iataCodes.text)
        listaAirlines.append(airlineCodes.text)
        listPaises.append(paises.text)


def start(bot, update, pass_chat_data = True):


    miID = update.message.chat.id
    c.append(str(miID))
    bot.sendMessage(chat_id = miID, text = '¡Hola! ¡Te habla el PanaMiguel 😹 y soy un bot interactivo!'
                                           '\nTe ayudaré a realizar correctamente la compra de tu boleto de vuelo'
                                           '\nElige tu opción, dando click al comando o escribiéndolo')

    bot.sendMessage(chat_id = miID, text = Menu)



def comprar(bot):
    global update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1

        if update.message:  # your bot can receive updates without messages
            # Reply to the message
            update.message.reply_text(update.message.text)










global update_id
update_id = None
TOKEN = '1275373802:AAGn8auWnyZWRjlDbO4zAD4446ThP5OSwbQ'
URL = "https://api.telegram.org/bot" + TOKEN + "/"
Menu = '¿Qué deseas hacer?: \n\n/Tutorial - Ver instrucciones \n/Comprar - Comprar vuelo  \n/Info - Información de aerolíneas y más \n/Cerrar chat\n\n'

bot = telegram.Bot("1275373802:AAGn8auWnyZWRjlDbO4zAD4446ThP5OSwbQ")
updater = Updater(TOKEN)
botUpdater = updater



listaIata = list()
listaAirlines = list()
listPaises = list()
mensajes = list()
c =  list()






datosAirlines()
start_handler = CommandHandler('start', start)
comprar_handler = CommandHandler('comprar', comprar)
dispatcher = botUpdater.dispatcher
dispatcher.add_handler(start_handler)
dispatcher.add_handler(comprar_handler)

botUpdater.start_polling()










