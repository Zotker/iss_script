## Локальные скрипты
import os
import sys

sys.path.append(os.path.abspath('./service'))

import access
import auth
from ruleon_array import data
## Библиотеки для работы скрипта
import requests
import json
import datetime

now = datetime.datetime.now()
counter = 1
header = { "Content-Type": "application/json" }

# Парсинг массива с данными

for parse_array in data:
	typicalconfig = parse_array[0]
	ruleid = parse_array[1]
	schedule = parse_array[2]
	scheduletemplate = parse_array[3]

	# Запрос информации для составления запроса

	schedule_get = auth.session.get(access.url + "/sem-restservices/db/schedule/" + str(schedule), headers=header)
	scheduletemplate_get = auth.session.get(access.url + "/sem-restservices/db/scheduletemplate/" + str(scheduletemplate), headers=header)
	typicalconfig_get = auth.session.get(access.url + "/sem-restservices/db/rule/child/typicalconfig/" + str(typicalconfig), headers=header)

	# Вытаскиваем id праивла из типовой конфигурации и формируем POST запрос

	for i in typicalconfig_get.json():
		if i['id'] == ruleid:
			buffer = i
			ruleid_get = json.dumps(buffer)
			constructor = '{"locked":false,' + '"rule":' + str(ruleid_get) + ', "schedule":' + str(schedule_get.text) + ', "template":' + str(scheduletemplate_get.text) + '}'
			data = json.loads(constructor)
			post = auth.session.post(access.url + "/sem-restservices/db/ruleon", json=data, headers=header)
			if post.status_code != 200:
				print(counter, "Правило по расписанию не добавлено по причине:")
				print(post.status_code, post.reason)
				print(post.text)
				counter += 1
			else:
				print(counter, "ok")
				counter += 1

print("Готово")