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

    return ELECCIONES


def datosPersonales(update, context):
    user_data = context.user_data
    text = update.message.text
    context.user_data['choice'] = text
    category = user_data['choice']
    if category == 'Confirmar compra':

        update.message.reply_text('👉 Por favor, llena los siguientes datos.', reply_markup = markupDatos)
    if category == 'Fechas':
        update.message.reply_text('👉 Por favor, ingresa los siguientes datos.', reply_markup = markupRetornos)

    if category == 'Fecha de ida':
        update.message.reply_text('👉 Por favor, ingresa los siguientes datos.', reply_markup=markupFechasFinal)

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
                                  .format(mensajeFinal(user_data)), reply_markup=markup)
    if category == 'Confirmar fecha':
        update.message.reply_text('selecciona', reply_markup = markupRetornos)
    return ELECCIONES


def done(update, context):
    update.message.reply_text('¡Espero haberte ayudado!\nNos vemos pronto.')
    #time.sleep(1.2)
    os.kill(os.getpid(), signal.SIGINT)
    return ConversationHandler.END


def mensajeFinal(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('👉 {} - {} \t✓'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])

def entradaDatos(update, context):
    user_data = context.user_data
    text = update.message.text
    context.user_data['choice'] = text
    update.message.reply_text(f'✈ {text}\n👉 Por favor, ingresa el dato para: {text}.')
    return REPLICAS


def eleccionMensaje(update, context): #funcionsssssssssssssssssssssssss
    user_data = context.user_data

    text = update.message.text
    context.user_data['choice'] = text
    del user_data['choice']
    update.message.reply_text("¡Muy bien! Estos son tus datos:"
                              "{}Puedes cambiar de dato cuando quieras, simplemente entra al botón que quieras."
        .format(mensajeFinal(user_data)),reply_markup=markup)


    return REPLICAeleccion


def receptorDatos(update, context):
    datosPersonales = ['Nombres','Apellidos', 'Celular','Pasaporte', 'Cédula', 'Domicilio']
    user_data = context.user_data
    text = update.message.text
    mensaje = text.upper()
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']
    if category == 'Origen' or category == 'Destino':
        if mensaje in listaIata:
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


    if category == 'Día' or category == 'Mes' or category == 'Año' or category == 'Día de regreso' or category == 'Mes de regreso' or category == 'Año de regreso':
        try:
            dato = int(text)
            if dato > 0 :
                #update.message.reply_text('😎 Se ha guardado la información.', reply_markup=markupFechasFinal)
                if category == 'Día':
                    if dato <= 30:
                        update.message.reply_text('😎 Se ha guardado la información.', reply_markup = markupFechasFinal)
                    else:
                        update.message.reply_text(f'❌ Error - El {category} debe ser menor a 31.\n👉 Ingresa nuevamente seleccionado el botón'
                                              f' {category}',reply_markup =markupFechasFinal)

                if category == 'Mes':
                    if dato <= 12:
                        update.message.reply_text('😎 Se ha guardado la información.', reply_markup = markupFechasFinal)
                    else:
                        update.message.reply_text(f'❌ Error - El {category} debe ser menor o igual a 12 (Diciembre).\n👉 Ingresa nuevamente seleccionado el botón'
                                              f' {category}',reply_markup =markupFechasFinal)

                if category == 'Año':
                    if dato <= 2021:
                        update.message.reply_text('😎 Se ha guardado la información.', reply_markup=markupFechasFinal)
                    else:
                        update.message.reply_text(
                            f'❌ Error - El {category} debe ser menor o igual a 2021.\n👉 Ingresa nuevamente seleccionado el botón'
                            f' {category}', reply_markup=markupFechasFinal)


            else:
                update.message.reply_text(f'❌ Error - El {category} no deber tener valores negativos.\n👉 Ingresa nuevamente seleccionado el botón'
                                          f' {category}',reply_markup =markupFechasFinal)
        except (ValueError):
            update.message.reply_text(f'❌ Error - El {category} no debe contener letras.\n👉 Ingresa nuevamente seleccionando el botón'
                f' {category}.', reply_markup=markupFechasFinal)
    return ELECCIONES



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

    botConversacion= ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ELECCIONES: [MessageHandler(Filters.regex('^(Origen|Destino|Pasajeros|Nombres'
                                                    '|Apellidos|Celular|Pasaporte|Cédula'
                                                    '|Domicilio|Día|Mes|Año|Día de regreso|Mes de regreso|Año de regreso)$'), entradaDatos),

                         MessageHandler(Filters.regex('^(Confirmar compra|Confirmar fecha|Fechas|Fecha de ida|Fecha de vuelta' 
                                                    '|Restaurar compra|Continuar)$'),
                                      datosPersonales),
                         ],
            REPLICAeleccion: [
                MessageHandler(Filters.text & ~(Filters.command | Filters.regex('^Done$') ),
                               datosPersonales)],

            REPLICAS: [
                MessageHandler(Filters.text & ~(Filters.command | Filters.regex('^Finalizar chat$')),
                               receptorDatos)],
        },

        fallbacks=[MessageHandler(Filters.regex('^Finalizar chat$'), done)]
    )

    dp.add_handler(botConversacion)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    ELECCIONES, REPLICAS, REPLICAeleccion= range(3)

    reply_keyboard = [['Origen', 'Destino', 'Fechas'],
                      ['Pasajeros', 'Confirmar compra', 'Restaurar compra'],
                      ['Finalizar chat']]
    reply_Datos = [['Nombres', 'Apellidos', 'Celular'], ['Pasaporte', 'Cédula', 'Domicilio'], ['Continuar']]


    reply_FechasFinal = [['Día', 'Mes', 'Año'], ['Confirmar fecha']]

    reply_Retornos = [['Fecha de ida', 'Fecha de vuelta']]

    reply_FechasIdaVelta = [['Día de regreso', 'Mes de regreso', 'Año de regreso'], ['Continuar']]

    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    markupDatos = ReplyKeyboardMarkup(reply_Datos, one_time_keyboard=True)

    markupRetornos = ReplyKeyboardMarkup(reply_Retornos, one_time_keyboard=True)

    markupFechasFinal = ReplyKeyboardMarkup(reply_FechasFinal, one_time_keyboard=True)

    markupFechasVuelta = ReplyKeyboardMarkup(reply_FechasIdaVelta, one_time_keyboard=True)
    listaIata = list()
    listaAirlines = list()
    listPaises = list()
    controlIdaVuelta = list()
    main()












