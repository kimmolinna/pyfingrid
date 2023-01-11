from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import json,urllib,requests

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get('https://oma.datahub.fi/')
input("Press any key to continue after authentication")
s = requests.Session()
s.cookies.update({c['name']: c['value'] for c in driver.get_cookies()})
driver.close()
auth = 'Bearer '+json.loads(urllib.parse.unquote(s.cookies.get_dict()['cap-user']))['token']
r = s.get('https://oma.datahub.fi/_api/GetAgreementData?agreementStatus=TRM',headers={'Authorization':auth})
print(r.content)