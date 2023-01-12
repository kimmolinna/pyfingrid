from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import json,urllib,requests,time

def get_token():
    driver = webdriver.Chrome(service = ChromeService(ChromeDriverManager().install()))
    driver.get('https://oma.datahub.fi/')
    count = 0
    user = None
    while count < 60:
        try:
            user = {c['name']: c['value'] for c in driver.get_cookies()}['cap-user']
            driver.close()
            break
        except:
            count += 1
            time.sleep(1)
    if user==None:
        raise Exception('Could not get token')
    else:
        return json.loads(urllib.parse.unquote(user))['token']
def get_metering_points(t : str):
    """Get metering points from the API

    Arguments:
        t -- The token from get_token()
    """
    s = requests.Session()
    r = s.get('https://oma.datahub.fi/_api/GetAgreementData?agreementStatus=TRM',headers={'Authorization': 'Bearer '+t})
    return r.content

token = get_token()
print(get_metering_points(token))