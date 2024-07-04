## Локальные скрипты
import os
import sys

sys.path.append(os.path.abspath('./service'))

import access
import auth
## Библиотеки для работы скрипта
import requests
import json
import os.path
import sys
import datetime
import codecs

# Счетчик (чтобы можно было сопоставить строку из excel)
now = datetime.datetime.now()
counter = 1
typicalconfig = []
header = { "Content-Type": "application/json" }

# Проверка наличия файла template.json
if os.path.isfile("rule_template/template.json"):
	pass
else:
	sys.exit('Отсутсвует файл шаблона "template.json"')

# Чтение JSON из файла
with codecs.open('rule_template/template.json', encoding="utf-8") as f:
	data = json.load(f)

# Обработчик добавления правил в ЛК
for i in data:
	response = auth.session.post(access.url + "/sem-restservices/db/rule", json=i, headers=header)
	if response.status_code != 200:
		print(counter, "Значение не добавлено по причине:")
		print(response.status_code, response.reason)
		print(response.text)
		print(i,"\n")
		counter += 1
	else:
		print(counter, "ok")
		counter += 1


for i in data:
	typicalconfig.append(i['typicalconfig']['id'])
unique_typicalconfig = list(set(typicalconfig))

# Запрос всех правил ЛК
response = auth.session.get(access.url + "/sem-restservices/db/rule")

# Проверка наличия директории для файла
if os.path.exists("rule_id"):
    pass
else:
    os.mkdir("./rule_id")

# Создание файла и запись всех правил по шаблону [id] [rulename]
with open("rule_id/rule_id.txt", "w") as f:
	for i in response.json():
		for j in unique_typicalconfig:
			if i['typicalconfig']['id'] == j: # поиск правил по id типовой конфигурации
				print(i['id'], i['rulename'], file=f)

print("Готово")