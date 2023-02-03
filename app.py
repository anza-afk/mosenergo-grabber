from telethon import TelegramClient, events
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
api_id   = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
entity = eval(config['Telegram']['entity'])
chats = eval(config['Telegram']['chats'])

with open('keywords.txt', 'r', encoding='utf-8') as keywords:
    kw_list = [line.replace('\n', '') for line in keywords]

client = TelegramClient('chat-grabber', api_id, api_hash)
client.start()

print('STARTED', f'Пересылаю из {chats} в {entity}', sep='\n')
print('Отслеживаю:', ', '.join(kw_list))

@client.on(events.NewMessage(chats=chats))
async def normal_handler(event):
    grabbed_string = str(event.message.message)
    if any(kw.lower() in grabbed_string.lower() for kw in kw_list):
        await client.send_message(entity=entity, message=grabbed_string)
        print(grabbed_string)
client.run_until_disconnected()