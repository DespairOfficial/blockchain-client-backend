from blockchain import BlockChain
import json
from pprint import pprint as print
link_client = 'https://b1.ahmetshin.com/static/blockchain.py'

username = 'ddss'
password ='2718'	
init = BlockChain(username=username, password=password, base_url = 'https://b1.ahmetshin.com/restapi/')
init.get_version_file()

# Регистрация пользователя
# result = init.register()
# print(result.json())

# Проверка монет
result = init.check_coins()
print(result.json())


result = init.get_chains()
print(result.json())

