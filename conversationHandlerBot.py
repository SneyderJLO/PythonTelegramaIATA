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
    precio = str(round(random.uniform(800, 12000), 2)) + " dólares"
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
    if category == 'Confirmar datos':
        del user_data['choice']
        update.message.reply_text(f"¡Muy bien! Estos son tus datos {mensajeFinal(user_data)}"
        f"\n👉 El valor del boleto de vuelo es: 💸 {precio}."
                                  , reply_markup=markup)

    if category == 'Confirmar fecha':
        update.message.reply_text('selecciona', reply_markup = markupRetornos)
    return ELECCIONES


def terminarBot(update, context):
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

def receptorDatos(update, context):
    datosPersonales = ['Nombres','Apellidos', 'Celular','Pasaporte', 'Cédula', 'Domicilio']
    user_data = context.user_data
    text = update.message.text
    mensaje = update.message.text.upper()
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']
    if category == 'Origen' or category == 'Destino':
        if mensaje in listaIata:
            indice = listaIata.index(mensaje)
            listaIata.pop(indice)
            update.message.reply_text(f'🌎 El país de {category} que elegiste es: {listPaises[indice]}.\n✈ La aerolínea es: {listaAirlines[indice]}.')
            user_data[category] = listPaises[indice]
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

                if category == 'Día':
                    if dato <= 30:
                        update.message.reply_text('😎 Se ha guardado la información.', reply_markup = markupFechasFinal)
                    else:
                        update.message.reply_text(f'❌ Error - El {category} debe ser menor a 31.\n👉 Ingresa nuevamente seleccionado el botón'
                                              f' {category}',reply_markup =markupFechasFinal)
                        del user_data['Día']

                if category == 'Mes':
                    if dato <= 12:
                        update.message.reply_text('😎 Se ha guardado la información.', reply_markup = markupFechasFinal)
                    else:
                        update.message.reply_text(f'❌ Error - El {category} debe ser menor o igual a 12 (Diciembre).\n👉 Ingresa nuevamente seleccionado el botón'
                                              f' {category}',reply_markup =markupFechasFinal)
                        del user_data['Mes']

                if category == 'Año':
                    if dato == 2020:
                        update.message.reply_text('😎 Se ha guardado la información.', reply_markup=markupFechasFinal)
                    else:
                        update.message.reply_text(
                            f'❌ Error - El {category} debe ser igual a 2020.\n👉 Ingresa nuevamente seleccionado el botón'
                            f' {category}', reply_markup=markupFechasFinal)
                        del user_data['Año']

                try:
                    if category == 'Día de regreso':
                        if dato >= int(user_data['Día']):
                            update.message.reply_text('😎 Se ha guardado la información.', reply_markup = markupFechasVuelta)
                        else:
                            update.message.reply_text(f'❌ Error - El {category} debe ser mayor al Día de Ida.\n👉 Ingresa nuevamente seleccionado el botón'
                                                      f' {category}',reply_markup =markupFechasVuelta)
                            del user_data['Día de regreso']


                    if category == 'Mes de regreso':
                        if dato  >= int(user_data['Mes']) and dato <=12:
                            update.message.reply_text('😎 Se ha guardado la información.', reply_markup = markupFechasVuelta)
                        else:
                            update.message.reply_text(f'❌ Error - El {category} debe ser mayor al Mes de Ida.\n👉 Ingresa nuevamente seleccionado el botón'
                                                  f' {category}',reply_markup =markupFechasVuelta)
                            del user_data['Mes de regreso']

                    if category == 'Año de regreso':
                        if dato == 2020:
                            update.message.reply_text('😎 Se ha guardado la información.', reply_markup=markupFechasVuelta)
                        else:
                            update.message.reply_text(
                                f'❌ Error - El {category} debe ser igual al Año de Ida.\n👉 Ingresa nuevamente seleccionado el botón'
                                f' {category}', reply_markup=markupFechasVuelta)
                            del user_data['Año de regreso']
                except KeyError:
                    update.message.reply_text('❌ Error - Aún no hay datos de la Fecha de Ida.\n👉 Ingresa uno seleccionando el botón Fecha de ida.',
                                              reply_markup=markupRetornos)


            else:
                update.message.reply_text(f'❌ Error - El {category} no deber tener valores negativos.\n👉 Ingresa nuevamente seleccionado el botón'
                                          f' {category}',reply_markup =markupFechasFinal)
                del user_data[category]
        except (ValueError):
            update.message.reply_text(f'❌ Error - El {category} no debe contener letras.\n👉 Ingresa nuevamente seleccionando el botón'
                f' {category}.', reply_markup=markupFechasFinal)
            del user_data[category]
    print(text)
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
                                                    '|Restaurar compra|Continuar|Confirmar datos)$'),
                                      datosPersonales),
                         ],
            REPLICAeleccion: [
                MessageHandler(Filters.text,datosPersonales)],

            REPLICAS: [
                MessageHandler(Filters.text,receptorDatos)],
        },

        fallbacks=[MessageHandler(Filters.regex('^Finalizar chat$'), terminarBot)]
    )

    dp.add_handler(botConversacion)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    ELECCIONES, REPLICAS, REPLICAeleccion= range(3)

    reply_keyboard = [['Origen', 'Destino', 'Fechas'],
                      ['Pasajeros', 'Confirmar compra', 'Restaurar compra'],
                      ['Finalizar chat']]
    reply_Datos = [['Nombres', 'Apellidos', 'Celular'], ['Pasaporte', 'Cédula', 'Domicilio'], ['Confirmar datos']]


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
