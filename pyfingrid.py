from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import json,requests,time
import urllib.parse

def get_cookies():
    """Get a token from the Fingrid datahub API

    Raises:
        Exception: If login is not successful in 60 seconds

    Returns:
        str -- The token
    """
    driver = webdriver.Chrome(service = ChromeService(ChromeDriverManager().install()))
    driver.get('https://oma.datahub.fi/')
    count = 0
    cookies = None
    while count < 60:
        count += 1
        time.sleep(1)
        if driver.current_url == 'https://oma.datahub.fi/#/':
            cookies = {c['name']: c['value'] for c in driver.get_cookies()}
            break
    if cookies==None:
        raise Exception('Could not get cookies')
    else:
        return cookies
def get_token(c : dict):
    """Get a token from the Fingrid datahub API cookies
    
    Arguments:
        c {dict} -- Cookies
    
    Returns:
        str -- The token
    """
    return json.loads(urllib.parse.unquote(c['cap-user']))['token']
def get_session(c: dict):
    """Login to the Fingrid datahub API with a token

    Arguments:
        t -- The token

    Returns:
        requests.Session -- Session object
    """
    s = requests.Session()
    s.cookies.update(c)
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