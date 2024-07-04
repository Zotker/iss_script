import requests
import json
import sys
import os
import datetime

current_date = datetime.datetime.now().strftime("%d%m%Y")

# Таблица удаления запрещенных символов из названий архивов
trans_table = {ord('\\') : None, ord('/') : None, ord(':') : None, ord('*') : None, ord('?') : None, ord('"') : None, ord('<') : None, ord('>') : None, ord('|') : None}

# Передача заголовка
header = { "Content-Type": "application/json" }

# Чтение файла instance.json для получения информации об инстансе
with open('instance.json', encoding="utf-8") as file:
	instance = json.load(file)

# Цикл обработки инстансов
	for instace_loop in instance:

		os.mkdir(current_date + "_" + instace_loop["instance"])
		
		# Авторизация в инстансе

		session = requests.Session()
		data = {"username": instace_loop["username"], "password": instace_loop["password"]}
		response = session.post(instace_loop["url"] + "/sem-restservices/auth/login", data=data)
		
		# Смена комании пользователя

		company_id = []
		company_name = []

		response = session.get(instace_loop["url"] + "/sem-restservices/db/user/profile/company", headers=header)

		for i in response.json():
			company_id.append(i["id"])
			company_name.append(i["name"])

		for company_switch_loop, company_name_loop in zip(company_id, company_name):
			response = session.post(instace_loop["url"] + "/sem-restservices/db/user/profile/company/switch?companyId=" + str(company_switch_loop) , headers=header)

			os.mkdir(current_date + "_" + instace_loop["instance"] + "/" + str(company_name_loop))

			print(company_switch_loop)

			# Выгрузка объектов инстанса
	
			objectid = []
			shortname = []
			
			response = session.get(instace_loop["url"] + "/sem-restservices/db/object", headers=header)
	
			os.mkdir(current_date + "_" + instace_loop["instance"] + "/" + str(company_name_loop) + "/object")
			
			for i in response.json():
				objectid.append(i["id"])
				shortname.append(i["shortname"])
			
			
			for j, k in zip(objectid, shortname):
				constructor = '{"devices":null,"typicalconfigs":null,"iconsets":null,"users":null,"objects":[' + str(j) + '],"dashboards":null}'
				data = json.loads(constructor)
			
				download = session.post(instace_loop["url"] + "/sem-restservices/db/expimp/export", json=data, headers=header)
	
				file = open (f'./{current_date}_{instace_loop["instance"]}/{company_name_loop}/object/{k.translate(trans_table)[0:150]}.zip', "wb")
				file.write(download.content)
				file.close()
	
			# Выгрузка дашбордов
	
			dash_id = []
			dashname = []
			
			response = session.get(instace_loop["url"] + "/sem-restservices/wg/dashboard", headers=header)
	
			os.mkdir(current_date + "_" + instace_loop["instance"] + "/" + str(company_name_loop) + "/dashboard")
			
			for i in response.json():
				dash_id.append(i["id"])
				dashname.append(i["dashname"])
	
			for j, k in zip(dash_id, dashname):
				constructor = '{"devices":null,"typicalconfigs":null,"iconsets":null,"users":null,"objects":null,"dashboards":[' + str(j) + ']}'
				data = json.loads(constructor)
	
				download = session.post(instace_loop["url"] + "/sem-restservices/db/expimp/export", json=data, headers=header)
	
				file = open (f'./{current_date}_{instace_loop["instance"]}/{company_name_loop}/dashboard/{k.translate(trans_table)[0:150]}.zip', "wb")
				file.write(download.content)
				file.close()	