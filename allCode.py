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
Menu = '¿Qué deseas hacer?: \n\n/Comprar vuelo  \n/Info - Acerca de nosotros \n\n'

bot = telegram.Bot(token = '1275373802:AAGn8auWnyZWRjlDbO4zAD4446ThP5OSwbQ')
mibot = telebot.TeleBot(TOKEN)
updater = Updater(TOKEN)
botUpdater = updater


def datosAirlines():
    sitioCodes = 'https://madavan.com.mx/codigo-iata-aerolineas/'
    pagina = requests.get(URL)
    soup = BeautifulSoup(pagina.content, 'html.parser')


def start(bot, update, pass_chat_data = True):

    miID = update.message.chat.id
    c.append(str(miID))
    bot.sendMessage(chat_id = miID, text = '¡Hola! ¡Te habla el PanaMiguel 😹 y soy un bot interactivo!'
                                           '\nTe ayudaré a realizar correctamente la compra de tu boleto de vuelo'
                                           '\nElige tu opción, dando click al comando o escribiéndolo')

    bot.sendMessage(chat_id = miID, text = Menu)


def comprar(bot, update):
    miID = update.message.chat.id
    bot.sendMessage(chat_id = miID, text = 'Aqui vas a comprar xd')



listaIata = list()
listaAirlines = list()
listPaises = list()
c =  list()
start_handler = CommandHandler('start', start)
comprar_handler = CommandHandler('comprar', comprar)
dispatcher = botUpdater.dispatcher
dispatcher.add_handler(start_handler)
botUpdater.start_polling()
dispatcher.add_handler(comprar_handler)

botUpdater.idle()


while True:
    pass





