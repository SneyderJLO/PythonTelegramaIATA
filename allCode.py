import threading as th
import telebot
from telebot import types
import time
import json
import requests
import telegram
from telegram.ext import *
TOKEN = '1275373802:AAGn8auWnyZWRjlDbO4zAD4446ThP5OSwbQ'
URL = "https://api.telegram.org/bot" + TOKEN + "/"
Menu = '¿Qué deseas hacer?: \n\n/Buscar  \n/info - Informacion De interes \n/hola - Saludo del Bot \n/piensa3D - Informacion sobre Piensa3D \n\n'

bot = telegram.Bot(token = '1275373802:AAGn8auWnyZWRjlDbO4zAD4446ThP5OSwbQ')
updater = Updater(TOKEN)
botUpdater = updater

def start(bot, update, pass_chat_data = True):
    update.message.chat.id
    bot.sendMessage(chat_id = update.message.chat.id, text = Menu)

start_handler = CommandHandler('start', start)
dispatcher = botUpdater.dispatcher
dispatcher.add_handler(start_handler)
botUpdater.start_polling()
botUpdater.idle()

while True:
    pass






