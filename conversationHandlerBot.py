import os
import signal
import  random
from bs4 import BeautifulSoup
import requests
import time
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
from telegram import ReplyKeyboardMarkup
CHOOSING, TYPING_REPLY, TYPING_CHOICE, DATOS = range(4)

reply_keyboard = [['Origen', 'Destino', 'Fechas'],
                  ['Pasajeros', 'Confirmar compra', 'Restaurar compra'],
                  ['Finalizar chat']]
reply_Datos = [['Nombres','Apellidos', 'Celular'], ['Pasaporte', 'Cédula', 'Domicilio'],['Continuar']]

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

markupDatos = ReplyKeyboardMarkup(reply_Datos, one_time_keyboard=True)

def start(update, context):
   update.message.reply_text('¡Hola! ¡Te habla el PanaMiguel 😹 y soy un bot interactivo!'
                                       '\nTe ayudaré a realizar correctamente la compra de tu boleto de vuelo.'
                                       '\nElige tu opción', reply_markup=markup)
   return CHOOSING


def datosPersonales(update, context):
    update.message.reply_text('👉 Por favor, llena los siguientes datos.', reply_markup = markupDatos)
    return CHOOSING

def done(update, context):
    update.message.reply_text('¡Espero haberte ayudado!\nNos vemos pronto.')
    time.sleep(1.2)
    os.kill(os.getpid(), signal.SIGINT)
    '''user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text("I learned these facts about you:"
                              "{}"
                              "Until next time!".format(facts_to_str(user_data)))

    user_data.clear()'''
    return ConversationHandler.END


def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('👉 {} - {} \t✓'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])

def regular_choice(update, context):
    user_data = context.user_data
    text = update.message.text
    context.user_data['choice'] = text
    category = user_data['choice']
    #if category == 'Origen' or category == 'Destino':
    update.message.reply_text(f'✈ {text}\n👉 Por favor, ingresa el dato para: {text}.')

    return TYPING_REPLY


def custom_choice(update, context):
    user_data = context.user_data

    text = update.message.text
    context.user_data['choice'] = text
    del user_data['choice']
    update.message.reply_text("¡Muy bien! Estos son tus datos:"
                              "{}Puedes cambiar de dato cuando quieras, simplemente entra al botón que quieras."
        .format(facts_to_str(user_data)),reply_markup=markup)


    return TYPING_CHOICE

def restaurarCompra(update,context):
    user_data = context.user_data
    user_data.clear()
    time.sleep(1.3)
    update.message.reply_text('¡Listo! Todos los datos han sido borrados.',reply_markup=markup)
    print(user_data)
    return ConversationHandler.END

def received_information(update, context):
    datosPersonales = ['Nombres','Apellidos', 'Celular','Pasaporte', 'Cédula', 'Domicilio']
    user_data = context.user_data
    text = update.message.text.upper()
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']
    if category == 'Origen' or category == 'Destino':
        if text in listaIata:
            indice = listaIata.index(text)
            listaIata.pop(indice)
            update.message.reply_text(f'🌎 El país de {category} que elegiste es: {listPaises[indice]}.\n✈ La aerolínea es: {listaAirlines[indice]}.')
            time.sleep(1)
            update.message.reply_text('😎 Se ha guardado la información.',reply_markup=markup)
        else:

             update.message.reply_text(f'❌ Error - El código no existe o ya lo escogiste.\n🔁 Ingresa de nuevo el dato seleccionado el botón {category}.',
                                          reply_markup=markup)
    if category in datosPersonales:
        update.message.reply_text('😎 Se ha guardado la información.', reply_markup=markupDatos)

    if category == 'Pasajeros':
        try:
            x = int(text)
            if x > 0:
                update.message.reply_text('😎 Se ha guardado la información.', reply_markup=markup)
            else:
                update.message.reply_text(f'❌ Error - La cantidad de pasajeros no deber tener valores negativos.\n👉 Ingresa nuevamente seleccionado el botón'
                                          f' {category}',reply_markup =markup )
        except ValueError:
            update.message.reply_text(f'❌ Error - La cantidad de pasajeros no debe tener una letra.\n👉 Ingresa nuevamente seleccionando el botón'
                                      f' {category}.', reply_markup =markup)
    return CHOOSING



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

def main():
    print(reply_Datos[0])
    datosAirlines()

    updater = Updater("1275373802:AAGn8auWnyZWRjlDbO4zAD4446ThP5OSwbQ", use_context=True)


    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSING: [MessageHandler(Filters.regex('^(Origen|Destino|Fechas|Pasajeros|Nombres'
                                                    '|Apellidos|Celular|Pasaporte|Cédula|Domicilio)$'),regular_choice),
                       MessageHandler(Filters.regex('^Confirmar compra$'),
                                      datosPersonales),
                       MessageHandler(Filters.regex('^Continuar$'),custom_choice),
                       MessageHandler(Filters.regex('Restaurar compra$'),restaurarCompra)
                       ],
            #DATOS: [MessageHandler(Filters.regex('^(Nombres|Apellidos)$'), regular_choice)],

            TYPING_CHOICE: [
                MessageHandler(Filters.text & ~(Filters.command | Filters.regex('^Done$')),
                               regular_choice)],

            TYPING_REPLY: [
                MessageHandler(Filters.text & ~(Filters.command | Filters.regex('^Finalizar chat$')),
                               received_information)],
        },

        fallbacks=[MessageHandler(Filters.regex('^Finalizar chat$'), done)]
    )

    dp.add_handler(conv_handler)


    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    listaIata = list()
    listaAirlines = list()
    listPaises = list()
    main()



