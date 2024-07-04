import os
import sys

sys.path.append(os.path.abspath('./service'))

import access
import auth
from attr_array import array
## Библиотеки для работы скрипта
import requests
import json

counter = 1
header = { "Content-Type": "application/json" }

for parse_array in array:
	obj = parse_array[0]
	attr = parse_array[1]
	value = parse_array[2]
	for i, j, k in zip(obj, attr, value):
		get_attr = auth.session.get(access.url + "/sem-restservices/attr/" + str(j))
		constructor = '{"attr":' + get_attr.text + ',"value":"' + str(k) + '"}'
		data = json.loads(constructor)
		post = auth.session.post(access.url + "/sem-restservices/attrval/" + str(i), json=data, headers=header)
	if post.status_code != 200:
			print(counter, "Действие не добавлено по причине:")
			print(post.status_code, post.reason)
			print(post.text)
			counter += 1
	else:
			print(counter, "ok")
			counter += 1