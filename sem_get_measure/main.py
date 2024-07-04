import os
import sys

sys.path.append(os.path.abspath('./service'))

import access
import auth
## Библиотеки для работы скрипта
from cdpid import cdpid
import requests
import json

header = { "Content-Type": "application/json" }

for i in cdpid:
	payload = { "cdpId": i, "from": 1706597400000, "to": 1706598000000, "limit": 1 }
	info = auth.session.get(access.url + "/sem-restservices/measure/period", params=payload, headers=header)
	file = open("output.txt", "a")
	file.write(str(i) + info.text + "\n")
file.close()