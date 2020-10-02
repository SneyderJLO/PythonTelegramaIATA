#print([u.message.chat_id for u in updates])
import telegram

mensajes = list()
bot_token = '1275373802:AAGn8auWnyZWRjlDbO4zAD4446ThP5OSwbQ'
bot = telegram.Bot(bot_token)
#print(bot.get_me())


flag = False
print('ingresa valor corecot')
while flag == False:
    updates = bot.get_updates()
    [mensajes.append(u.message.text) for u in updates]
    if mensajes[-1] == 'jajasaplls':
        print('Pertenece a la ciudad LOJA')
        flag = True
    else:
        updates = bot.get_updates()
        [mensajes.append(u.message.text) for u in updates]





#print(updates[len(updates)-1])


'''
    if mensajes[-1] == 'jajasapll':
        print('Pertenece a la ciudad LOJA')
        flag = True

    else:
        flag = False
        print('Debes ingresar valores correctos')
        updates = bot.get_updates()
        [mensajes.append(u.message.text) for u in updates]
        break

'''

while True:
    origen = update.message.text.upper()
    if origen in listaIata:
        indice = listaIata.index(origen)
        update.message.reply_text(
            f'🌎El país de origen que elegiste es: {listPaises[indice]}.\n✈La aerolínea es: {listaAirlines[indice]}')
        update.message.reply_text('Escribe - 1 - para confirmar\nEscribe - 0 - para seleccionar otro origen')
        # dp.add_handler(MessageHandler(Filters.text, validacion(opcion, update)))

        break
    else:
        update.message.reply_text('No coincide el código')
        break




    try:
        while opcion != 1:
            opcion = int(update.message.text)
            if opcion == 0:
                comprar()
            else:
                update.message.reply_text('Vuelve a ingresar')
    except ValueError:
        update.message.reply_text('Error, debes ingresar solo dígitos')