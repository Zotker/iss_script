import requests
import json
import sys
import os
import datetime
import time
import subprocess
import asyncio

# https://stackoverflow.com/questions/39455022/python-3-print-update-on-multiple-lines
UP = "\x1B[9A"
CLR = "\x1B[0K"
# Передача заголовка
header = { "Content-Type": "application/json" }

# Чтение файла instance.json для получения информации об инстансе
with open('instance.json', encoding="utf-8") as file:
	instance = json.load(file)

# Аутентификация
session = requests.Session()
data = {"username": str(instance[0]["username"]), "password": str(instance[0]["password"])}
response = session.post(str(instance[0]["url"]) + "/sem-restservices/auth/login", data=data)

# Смена компании
response = session.post(str(instance[0]["url"]) + "/sem-restservices/db/user/profile/company/switch?companyId=" + "1", headers=header)

# Очистка окна терминала
subprocess.run(["clear"])
	
# Вывод информации в окно терминала
async def data():
	while True:
		serv_temp = session.get(str(instance[0]["url"]) + "/sem-restservices/db/contrdeviceparam/744062", headers=header)
		serv_humidity = session.get(str(instance[0]["url"]) + "/sem-restservices/db/contrdeviceparam/744063", headers=header)
		shit_temp = session.get(str(instance[0]["url"]) + "/sem-restservices/db/contrdeviceparam/744066", headers=header)
		shit_humidity = session.get(str(instance[0]["url"]) + "/sem-restservices/db/contrdeviceparam/744067", headers=header)
		print(f"{UP}\nСерверная:{CLR}\nТемпература: {serv_temp.json()['curvalue']}{CLR}\nВлажность: {serv_humidity.json()['curvalue']}%{CLR}\n{CLR}\nЩитовая:{CLR}\nТемпература: {shit_temp.json()['curvalue']}{CLR}\nВлажность: {shit_humidity.json()['curvalue']}%{CLR}\n")
		await asyncio.sleep(210)
	
async def current_date():
	while True:
		date = datetime.datetime.now()
		now = date.strftime('%d-%m-%y %H:%M:%S')
		print(f"{UP}{now}{CLR}")
		await asyncio.sleep(1)

async def main():

	await asyncio.gather(data(), current_date())

if __name__ == "__main__":
	  asyncio.run(main())