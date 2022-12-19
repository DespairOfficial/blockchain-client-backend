import datetime
import multiprocessing
from typing import Union
from fastapi import FastAPI
import uvicorn
from blockchain import BlockChain
from pydantic import BaseModel
import json
from pprint import pprint 
import time
from fastapi.middleware.cors import CORSMiddleware
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
link_client = 'https://b1.ahmetshin.com/static/blockchain.py'

username = 'dds'
password ='2718'	
init = BlockChain(username=username, password=password, base_url = 'https://b1.ahmetshin.com/restapi/')
#d68ee9c88a4edc37212dc0104364d7c76e69c02ede4b231b29d5f84c09ea4603	file_hash
#148289c8597625c9a756fed7fb547a33cb02b835115b334bd2fbc47ff45547b9 	user_hash
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

multiprocessing.freeze_support()


    

def solve(task,i):
    id = task['id']
    data_json = task['data_json']
    hash = init.get_hash_object(json.dumps(data_json))
    result_hash = init.make_hash(hash)
    data = {
        'type_task':'BlockTaskUser_Solution',
        'id':id,
        'hash':result_hash
    }
    print(init.send_task(data).json()) 
    print('Task id:', id)
    print('Process num:', i)

def multiproc(tasks):
    process_pool = []
    for i,task in enumerate(tasks):
        t = multiprocessing.Process(target=solve, args=(task, i))
        t.start()
        process_pool.append(t)
    for t in process_pool:
        t.join()

while True:
    time.sleep(2)
    print(f'sleep {str(datetime.datetime.now())}')
    
    # Получаем цепочки какие есть, и сохраняем у себя локально
    result = init.get_chains()
    # print(result.json())
    
    # получаем задачи, которые надо решить
    result = init.get_task().json()
    
    # проверяем какие задачи поступили на решение
    if result['tasks']:
        tasks_arr = []
        for task in result['tasks']:
            if(not task['status_solution']):
                tasks_arr.append(task)
                if(len(tasks_arr)==5):
                    multiproc(tasks_arr)
                    tasks_arr= []
                    break
        multiproc(tasks_arr)


    