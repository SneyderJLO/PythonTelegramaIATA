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