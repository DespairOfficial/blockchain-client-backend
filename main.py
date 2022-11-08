from typing import Union
from fastapi import FastAPI
import uvicorn
from blockchain import BlockChain
from pydantic import BaseModel
import json
from pprint import pprint as print
from fastapi.middleware.cors import CORSMiddleware
link_client = 'https://b1.ahmetshin.com/static/blockchain.py'

username = 'dds'
password ='2718'	
init = BlockChain(username=username, password=password, base_url = 'https://b1.ahmetshin.com/restapi/')
#d68ee9c88a4edc37212dc0104364d7c76e69c02ede4b231b29d5f84c09ea4603	file_hash
#7945c49c04420e01eb74491ce82f1f1c5b6966af877744a5361e275a943c5e96 	user_hash
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


class DataType(BaseModel):
    type_task : str
    from_hach : str
    to_hach : str
    count_coins : int

    class Config:
        orm_mode = True 

@app.post('/send_task')
def send_task(dataType: DataType):
    data = {
        'type_task': dataType.type_task,
        'from_hach': dataType.from_hach,
        'to_hach': dataType.to_hach,
        'count_coins': dataType.count_coins
    }
    result = init.send_task(data)
    return result.json()

if __name__ == "__main__":
    uvicorn.run('main:app', port= 8000, host="0.0.0.0", reload=True)