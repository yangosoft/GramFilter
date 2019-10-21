import configparser
import json
from datetime import date, datetime
import asyncio
import time
loop = asyncio.get_event_loop()
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import  PeerChannel


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        if isinstance(o, bytes):
            return list(o)

        return json.JSONEncoder.default(self, o)


config = configparser.ConfigParser()
config.read("config.ini")

api_id = config['Telegram']['api_id']
api_hash = str(config['Telegram']['api_hash'])

phone = config['Telegram']['phone']
username = config['Telegram']['username']


client = TelegramClient(username, api_id, api_hash).start()

me = asyncio.get_event_loop().run_until_complete(client.get_me())
lstChannels = [x.strip() for x in config['Telegram']['lst_channels'].split(',')]
topics =  [x.strip() for x in  config['Telegram']['topics'].split(',')]
messages = []

while (True):
    for channel in lstChannels:
        try:
            if channel.isdigit():
                entity = PeerChannel(int(channel))
            else:
                entity = channel
            my_channel = asyncio.get_event_loop().run_until_complete(client.get_entity(entity))
        except:
            continue

        msgs = asyncio.get_event_loop().run_until_complete(client.get_messages(my_channel, limit=100))
        for m in msgs:
            if (m.message is not None):
                for t in topics:
                    if ( m.message.find(t) > -1 ):
                        if m.message not in messages:
                            messages.append(m.message)
                            print(m)
                            asyncio.get_event_loop().run_until_complete(client.send_message('me',m))
                            break
    print(messages)
    time.sleep(60 * 5)
