## Локальные скрипты
import os
import sys

sys.path.append(os.path.abspath('./service'))

import access
import auth
from ruleaction_array import data
## Библиотеки для работы скрипта
import requests
import json
import datetime

now = datetime.datetime.now()
counter = 1
header = { "Content-Type": "application/json" }


# Чтение переменной data из файла ruleaction_array, добавление массивов в переменные
for parse_array in data:
	rule = parse_array[0]
	deviceparam = parse_array[1]
	action = parse_array[2]
	# Парсинг массива и выполнение обработки
	for i in rule:
		rule_get = auth.session.get(access.url + "/sem-restservices/db/rule/" + str(i), headers=header)
		for j, k in zip(deviceparam, action):
			deviceparam_get = auth.session.get(access.url + "/sem-restservices/db/deviceparam/" + str(j), headers=header)
			constructor = '{"action":"' + str(k) + '", "deviceparam":' + deviceparam_get.text + ', "rule":' + rule_get.text + ', "root": true' +'}'
			data = json.loads(constructor)
			post = auth.session.post(access.url + "/sem-restservices/db/ruleaction", json=data, headers=header)
		if post.status_code != 200:
			print(counter, "Действие не добавлено по причине:")
			print(post.status_code, post.reason)
			print(post.text)
			counter += 1
		else:
			print(counter, "ok")
			counter += 1

print("Готово")