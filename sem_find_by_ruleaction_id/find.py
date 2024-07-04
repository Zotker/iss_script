import os
import sys

sys.path.append(os.path.abspath('./service'))

import access
import auth
## Библиотеки для работы скрипта
import requests
import json

header = { "Content-Type": "application/json" }

ruleaction_id = input("Введите RuleActionID: ")

# Получение информации о команиях
company_id = []
company_name = []
get_company = auth.session.get(access.url + "/sem-restservices/company")
	
for i in get_company.json():
	company_id.append(i["id"])
	company_name.append(i["name"])

# Смена компании и поиск необходимого RuleActionID.
for company_id_swith, company_name_switch in zip(company_id, company_name):
	response = auth.session.post(access.url + "/sem-restservices/db/user/profile/company/switch?companyId=" + str(company_id_swith) , headers=header)
	response_ruleaction = auth.session.get(access.url + "/sem-restservices/db/ruleaction/" + ruleaction_id)
	if response_ruleaction.status_code == 200:
		print()
		print("CompanyName:", company_name_switch)
		print("RuleID:", response_ruleaction.json()['rule']['id'])
		print("TypicalConfig:", response_ruleaction.json()['rule']['typicalconfig']['id'])
		print("TypicalConfig_name:", response_ruleaction.json()['rule']['typicalconfig']['configname'])
		print("TypicalConfig_comment:", response_ruleaction.json()['rule']['typicalconfig']['comment'])