import os
import signal
import  random
from bs4 import BeautifulSoup
import requests
import time
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
from telegram import ReplyKeyboardMarkup


def start(update, context):
    update.message.reply_text('¡Hola! ¡Te habla el PanaMiguel 😹 y soy un bot interactivo!'
                                       '\nTe ayudaré a realizar correctamente la compra de tu boleto de vuelo.'
                                        '\n✈ Si no conoces el código, puedes visitar \n👉 https://madavan.com.mx/codigo-iata-aerolineas/ 👈')
    #time.sleep(1) ---------------
    update.message.reply_text('👉 Elige tu opción', reply_markup=markup)

    return CHOOSING


def datosPersonales(update, context):
    user_data = context.user_data
    text = update.message.text
    context.user_data['choice'] = text
    category = user_data['choice']
    if category == 'Confirmar compra':

        update.message.reply_text('👉 Por favor, llena los siguientes datos.', reply_markup = markupDatos)
    if category == 'Fechas':
        update.message.reply_text('👉 Por favor, ingresa los siguientes datos.', reply_markup = markupFechas)
    if category == 'Solo ida':
        reply_FechasFinal = [['Día', 'Mes', 'Año'], ['Continuar']]

        markupFechasFinal = ReplyKeyboardMarkup(reply_FechasFinal, one_time_keyboard=True)
        update.message.reply_text('👉 Por favor, ingresa los siguientes datos.', reply_markup = markupFechasFinal)

    if category == 'Fecha de ida':
        reply_FechasFinal = [['Día', 'Mes', 'Año'], ['Confirmar fecha']]
        markupFechasFinal = ReplyKeyboardMarkup(reply_FechasFinal, one_time_keyboard=True)
        update.message.reply_text('👉 Por favor, ingresa los siguientes datos.', reply_markup=markupFechasFinal)
    if category == 'Ida y vuelta':
        controlIdaVuelta.append('flag')
        update.message.reply_text('👉 Por favor, ingresa los siguientes datos.', reply_markup = markupRetornos)

    if category == 'Fecha de vuelta':
        update.message.reply_text('👉 Por favor, ingresa los siguientes datos.', reply_markup = markupFechasVuelta)

    if category == 'Restaurar compra':
        update.message.reply_text('¡Listo! Todos los datos han sido borrados.', reply_markup=markup)
        user_data.clear()
        #time.sleep(1)

    if category == 'Continuar':
        del user_data['choice']
        update.message.reply_text("¡Muy bien! Estos son tus datos:"
                                  "{}Puedes cambiar de dato cuando quieras, simplemente entra al botón que quieras."
                                  .format(facts_to_str(user_data)), reply_markup=markup)
    if category == 'Confirmar fecha':
        update.message.reply_text('selecciona', reply_markup = markupRetornos)
    return CHOOSING


def done(update, context):
    update.message.reply_text('¡Espero haberte ayudado!\nNos vemos pronto.')
    #time.sleep(1.2)
    os.kill(os.getpid(), signal.SIGINT)
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
    '''if category == 'Fecha de ida' or category == 'Fecha de vuelta':
        #del user_data['Fechas']
        update.message.reply_text('Por favor, ingresa el día, mes y año seguido de un espacio.\nEjemplo: 02 11 2020')
    else:'''
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

    if 'flag' in controlIdaVuelta:
        reply_FechasFinal = [['Día', 'Mes', 'Año'], ['Confirmar fecha']]
        markupFechasFinal = ReplyKeyboardMarkup(reply_FechasFinal, one_time_keyboard=True)
        controlIdaVuelta.clear()
    if category == 'Día' or category == 'Mes' or category == 'Año':
        try:
            dato = int(text)
            if dato > 0 :
                update.message.reply_text('😎 Se ha guardado la información.', reply_markup=markupFechasFinal)
            else:
                update.message.reply_text(f'❌ Error - El {category} no deber tener valores negativos.\n👉 Ingresa nuevamente seleccionado el botón'
                                          f' {category}',reply_markup =markupFechasFinal)
        except (ValueError):
            update.message.reply_text(f'❌ Error - El {category} no debe contener letras.\n👉 Ingresa nuevamente seleccionando el botón'
                f' {category}.', reply_markup=markupFechasFinal)
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
    datosAirlines()
    updater = Updater("1275373802:AAGn8auWnyZWRjlDbO4zAD4446ThP5OSwbQ", use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [MessageHandler(Filters.regex('^(Origen|Destino|Pasajeros|Nombres'
                                                    '|Apellidos|Celular|Pasaporte|Cédula'
                                                    '|Domicilio|Día|Mes|Año)$'),regular_choice),

                       MessageHandler(Filters.regex('^(Confirmar compra|Confirmar fecha|Fechas|Fecha de ida|Fecha de vuelta|Solo ida|Ida y vuelta|Restaurar compra|Continuar)$'),
                                      datosPersonales),
                       ],
            TYPING_CHOICE: [
                MessageHandler(Filters.text & ~(Filters.command | Filters.regex('^Done$') ),
                               datosPersonales)],

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
    CHOOSING, TYPING_REPLY, TYPING_CHOICE, DATOS = range(4)

    reply_keyboard = [['Origen', 'Destino', 'Fechas'],
                      ['Pasajeros', 'Confirmar compra', 'Restaurar compra'],
                      ['Finalizar chat']]
    reply_Datos = [['Nombres', 'Apellidos', 'Celular'], ['Pasaporte', 'Cédula', 'Domicilio'], ['Continuar']]

    replyFechasInicial = [['Solo ida', 'Ida y vuelta']]

    reply_FechasFinal = [['Día', 'Mes', 'Año'], ['Continuar']]

    reply_Retornos = [['Fecha de ida', 'Fecha de vuelta']]

    reply_FechasIdaVelta = [['Día (Regreso)', 'Mes (Regreso)', 'Año (Regreso)'], ['Continuar']]

    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    markupDatos = ReplyKeyboardMarkup(reply_Datos, one_time_keyboard=True)

    markupFechas = ReplyKeyboardMarkup(replyFechasInicial, one_time_keyboard=True)

    #markupFechasFinal = ReplyKeyboardMarkup(reply_FechasFinal, one_time_keyboard=True)

    markupRetornos = ReplyKeyboardMarkup(reply_Retornos, one_time_keyboard=True)

    markupFechasVuelta = ReplyKeyboardMarkup(reply_FechasIdaVelta, one_time_keyboard=True)
    listaIata = list()
    listaAirlines = list()
    listPaises = list()
    controlIdaVuelta = list()
    main()












