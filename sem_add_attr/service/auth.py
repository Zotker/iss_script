## Локальные скрипты
import access
## Библиотеки для работы скрипта
import requests

## Авторизация
session = requests.Session()
data = {"username": access.login, "password": access.password}
response = session.post(access.url + "/sem-restservices/auth/login", data=data)

if response.status_code == 200:
	print("Выполнено подключение\n")
else:
	print("Ошибка", response.status_code)