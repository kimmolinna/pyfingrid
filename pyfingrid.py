from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import json,requests,time
import urllib.parse

def get_token():
    """Get a token from the Fingrid datahub API

    Raises:
        Exception: If login is not successful in 60 seconds

    Returns:
        str -- The token
    """
    driver = webdriver.Chrome(service = ChromeService(ChromeDriverManager().install()))
    driver.get('https://oma.datahub.fi/')
    count = 0
    user = None
    while count < 60:
        try:
            user = {c['name']: c['value'] for c in driver.get_cookies()}['cap-user']
            break
        except:
            count += 1
            time.sleep(1)
    if user==None:
        raise Exception('Could not get token')
    else:
        return json.loads(urllib.parse.unquote(user))['token']
def login(t : str):
    """Login to the Fingrid datahub API with a token

    Arguments:
        t -- The token

    Returns:
        requests.Session -- Session object
    """
    s = requests.Session()
    r = s.get('https://oma.datahub.fi/',headers={'Authorization': 'Bearer '+t})
    return s
def get_metering_points(s : requests.Session, t : str):
    """Get metering points from the API

    Arguments:
        s {requests.Session} -- Session object
    """
    r = s.get('https://oma.datahub.fi/_api/GetAgreementData?agreementStatus=TRM',headers={'Authorization': 'Bearer '+t})
    return r.content
def logout(s : requests.Session):
    """Logout from the API
    
    Arguments:
        s {requests.Session} -- Session object
    """
    r = s.get('https://oma.datahub.fi/_api/logout')
    return r.ok
token = get_token()
session = login(token)
print(get_metering_points(session,token))
ok = logout(session)