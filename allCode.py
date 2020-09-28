import threading as th
import telebot
from telebot import types
import time
import json
import requests
import telegram
import telegram.ext

TOKEN = '1275373802:AAGn8auWnyZWRjlDbO4zAD4446ThP5OSwbQ'
URL = "https://api.telegram.org/bot" + TOKEN + "/"
Menu = '¿Qué deseas hacer?: \n\n/Buscar  \n/info - Informacion De interes \n/hola - Saludo del Bot \n/piensa3D - Informacion sobre Piensa3D \n\n'

bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['start'])
def update():
    # Llamar al metodo getUpdates del bot haciendo una peticion HTTPS (se obtiene una respuesta codificada)
    respuesta = requests.get(URL + "getUpdates")

    # Decodificar la respuesta recibida a formato UTF8 (se obtiene un string JSON)
    mensajes_js = respuesta.content.decode("utf8")

    # Convertir el string de JSON a un diccionario de Python
    mensajes_diccionario = json.loads(mensajes_js)

    # Devolver este diccionario
    return mensajes_diccionario

def leer_mensaje():

    # Llamar update() y guardar el diccionario con los mensajes recientes
    mensajes = update()

    # Calcular el indice del ultimo mensaje recibido
    indice = len(mensajes["result"]) - 1

    # Extraer el texto, nombre de la persona e id del último mensaje recibido
    texto = mensajes["result"][indice]["message"]["text"]
    persona = mensajes["result"][indice]["message"]["from"]["first_name"]
    id_chat = mensajes["result"][indice]["message"]["chat"]["id"]

    bot.send_message(id_chat, f'Hola{persona}, soy el bot PanaMiguel, y estoy aquí para ayudarte a comprar tu boleto de vuelo')
    bot.send_message(id_chat, Menu)

    #print(persona + " (id: " + str(id_chat) + ") ha escrito: " + texto)

def start(bot, update):
    update.message.reply_text("Hola, ¿En qué puedo ayudarte? 😀")


def main():

    updater = telegram.ext.Updater("512361253:AABCjU33hDwcsWV8n6Z9kYbBqLGhi3e-APc")
    dp = updater.dispatcher

    dp.add_handler(telegram.ext.CommandHandler("start", start))
    updater.start_polling()
    updater.idle()
if __name__ == '__main__':
    main()



