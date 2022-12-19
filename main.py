from typing import Union
from fastapi import FastAPI
import uvicorn
from blockchain import BlockChain
from pydantic import BaseModel
import json
from pprint import pprint as print
from fastapi.middleware.cors import CORSMiddleware
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
link_client = 'https://b1.ahmetshin.com/static/blockchain.py'

username = 'dds'
password ='2718'	
init = BlockChain(username=username, password=password, base_url = 'https://b1.ahmetshin.com/restapi/')

myHash = '148289c8597625c9a756fed7fb547a33cb02b835115b334bd2fbc47ff45547b9'
interlocutorHash = '6d22d1046aeffc8eb1fff1a32dd912a107277b05032c933ae05cbb9ee48b1f36'

#d68ee9c88a4edc37212dc0104364d7c76e69c02ede4b231b29d5f84c09ea4603	file_hash
#7945c49c04420e01eb74491ce82f1f1c5b6966af877744a5361e275a943c5e96 	
#148289c8597625c9a756fed7fb547a33cb02b835115b334bd2fbc47ff45547b9   user_hash

init.get_version_file()


app = FastAPI()
origins = [
	"*",
]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)
@app.get("/coins")
def read_root():
	result = init.check_coins()
	return result.json()

@app.get("/chains")
def read_root():
	result = init.get_chains()
	return result.json()



@app.get('/get_task')
def get_task():
	result = init.get_task()
	return result.json()


class SendCoins(BaseModel):
	type_task : str
	from_hach : str
	to_hach : str
	count_coins : int

	class Config:
		orm_mode = True 

class SendMessage(BaseModel):
	type_task : str
	from_hach : str
	to_hach : str
	message : str

	class Config:
		orm_mode = True 

@app.get('/get_my_messages')
def get_my_messages():
	password = 'DanilAndKamil'
	result = init.get_chains()
	object = result.json()
	messageItems = []

	for block in object['chains']['block_active']:
		for data in block['data_json']:
			if data['data_json']['type_task'] == 'custom' and data['data_json']['from_hach'] == myHash and data['data_json']['to_hach'] == interlocutorHash: 
				if('message' in data['data_json']):
					if(isinstance(data['data_json']['message'],str)):
						message = data['data_json']['message']
						messageItems.append({'sender': 'me', 'message': message})
					else:
						encryptedObject = data['data_json']['message']
						data = {
							'private_key': password,
							'encrypted_object': encryptedObject
						}
						result =  init.decrypt(data).json()['message']
						print(result)
						messageItems.append({'sender': 'me', 'message': result})

			elif data['data_json']['type_task'] == 'custom' and data['data_json']['from_hach'] == interlocutorHash and data['data_json']['to_hach'] == myHash: 
				if('message' in data['data_json']):
					if(isinstance(data['data_json']['message'],str)):
						message = data['data_json']['message']
						messageItems.append({'sender': 'other', 'message': message})
					else:
						encryptedObject = data['data_json']['message']
						data = {
							'private_key': password,
							'encrypted_object': encryptedObject
						}
						result =  init.decrypt(data).json()['message']
						messageItems.append({'sender': 'me', 'message': result})
					
	return messageItems

@app.post('/send_coins')
def send_coins(sendCoins: SendCoins):
	data = {
		'type_task': 'send_coins',
		'from_hach': sendCoins.from_hach,
		'to_hach': sendCoins.to_hach,
		'count_coins': sendCoins.count_coins
	}
	result = init.send_task(data)
	return result.json()

@app.post('/send_message')
def send_message(sendMessage: SendMessage):

	password = 'DanilAndKamil'

	messageObj = init.encrypt({
		'private_key': password,
		'text': sendMessage.message
	})
	

	data = {
		'type_task': 'custom',
		'from_hach': sendMessage.from_hach,
		'to_hach': sendMessage.to_hach,
		'message': messageObj.json()
	}
	result = init.send_task(data)
	return result.json()

if __name__ == "__main__":
	uvicorn.run('main:app', port= 8000, host="0.0.0.0", reload=True)



