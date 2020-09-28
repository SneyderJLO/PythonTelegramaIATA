import threading as th
import telebot
from telebot import types
import time
import json
import requests

TOKEN = '1275373802:AAGn8auWnyZWRjlDbO4zAD4446ThP5OSwbQ'
URL = "https://api.telegram.org/bot" + TOKEN + "/"
Menu = 'Puedes utilizar los siguientes comandos : \n\n/ayuda - Guia para utilizar el bot. \n/info - Informacion De interes \n/hola - Saludo del Bot \n/piensa3D - Informacion sobre Piensa3D \n\n'

tb = telebot.TeleBot(TOKEN)

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
    tb.send_message(id_chat, f'Hola{persona}, soy el bot PanaMiguel, y estoy aquí para ayudarte a comprar tu boleto de vuelo')
    #print(persona + " (id: " + str(id_chat) + ") ha escrito: " + texto)


# Llamar a la funcion "leer_mensaje()"
leer_mensaje()
