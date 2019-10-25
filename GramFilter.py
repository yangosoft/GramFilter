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



config = configparser.ConfigParser()
config.read("config.ini")

api_id = config['Telegram']['api_id']
api_hash = str(config['Telegram']['api_hash'])

phone = config['Telegram']['phone']
username = config['Telegram']['username']


client = TelegramClient(username, api_id, api_hash).start()

me = asyncio.get_event_loop().run_until_complete(client.get_me())
lstDialogs = asyncio.get_event_loop().run_until_complete(client.get_dialogs())
topics =  [x.strip() for x in  config['Telegram']['topics'].split(',')]
messages = []

while (True):
	username = config['Telegram']['username'].strip()
	topics =  [x.strip().lower() for x in  config['Telegram']['topics'].split(',')]
	lstDialogs = asyncio.get_event_loop().run_until_complete(client.get_dialogs())
	for channel in lstDialogs:
		print ("Accessing " + str(channel.title))
		print ("	|-> ID " + str(channel.id))
		if channel in entityId:
			my_channel = entityId[channel]
		else:
			try:
				entity = PeerChannel(int(channel.id))
				my_channel = asyncio.get_event_loop().run_until_complete(client.get_entity(channel.id))
				entityId[channel.title] = my_channel
				
			except Exception as e:
				print("Error joining info from " + channel.title)
				print("Unexpected error:", str(e))
				continue


		msgs = asyncio.get_event_loop().run_until_complete(client.get_messages(my_channel, limit=10))

		for m in msgs:
			if (m.message is not None):
				for t in topics:
					if ( m.message.lower().find(t) > -1 ):
						if m.message not in messages:
							messages.append(m.message)
							try:
								asyncio.get_event_loop().run_until_complete(client.send_message(username,m))
								time.sleep(5)
								messages.append(m.message)
							except:
								pass
								#asyncio.get_event_loop().run_until_complete(client.send_message('me',m))
							break

        
	time.sleep(60 * 5)