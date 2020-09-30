import threading as th
import telebot
from telebot import types
import time
import json
from bs4 import BeautifulSoup
import requests
import telegram
from telegram.ext import *
TOKEN = '1275373802:AAGn8auWnyZWRjlDbO4zAD4446ThP5OSwbQ'
URL = "https://api.telegram.org/bot" + TOKEN + "/"
Menu = '¿Qué deseas hacer?: \n\n/Tutorial - Ver instrucciones \n/Comprar - Comprar vuelo  \n/Info - Información de aerolíneas y más \n/Cerrar chat\n\n'

bot = telegram.Bot(token = '1275373802:AAGn8auWnyZWRjlDbO4zAD4446ThP5OSwbQ')
mibot = telebot.TeleBot(TOKEN)
updater = Updater(TOKEN)
botUpdater = updater


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


def start(bot, update, pass_chat_data = True):

    miID = update.message.chat.id
    c.append(str(miID))
    bot.sendMessage(chat_id = miID, text = '¡Hola! ¡Te habla el PanaMiguel 😹 y soy un bot interactivo!'
                                           '\nTe ayudaré a realizar correctamente la compra de tu boleto de vuelo'
                                           '\nElige tu opción, dando click al comando o escribiéndolo')

    bot.sendMessage(chat_id = miID, text = Menu)


def comprar(bot, update):


    miID = update.message.chat.id
    flag = False
    bot.sendMessage(chat_id=miID, text='por favor ingresa un dato')
    while flag == False:
        updates = bot.get_updates()
        [mensajes.append(u.message.text) for u in updates]
        if len(mensajes) > 0:
            flag = True
        else:
            updates = bot.get_updates()
            [mensajes.append(u.message.text) for u in updates]
    print(mensajes)
    print(listaIata)








listaIata = list()
listaAirlines = list()
listPaises = list()
mensajes = list()
c =  list()
texto = ''
datosAirlines()
start_handler = CommandHandler('start', start)
comprar_handler = CommandHandler('comprar', comprar)
dispatcher = botUpdater.dispatcher
dispatcher.add_handler(start_handler)
botUpdater.start_polling()
dispatcher.add_handler(comprar_handler)

botUpdater.idle()



while True:
    pass





