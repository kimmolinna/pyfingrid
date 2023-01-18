from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import json,requests,time
import urllib.parse

def get_cookies(file : str = "")->dict:
    """Get cookies for the Fingrid datahub API from the file or with Selenium and ChromeDriver

    Arguments:
        file {str} -- Path to the file containing the cookies (default: {""})
    
    Raises:
        Exception: If login is not successful in 60 seconds

    Returns:
        dict -- Cookies
    """
    if file == "":
        chrome = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service = chrome)
        driver.get('https://oma.datahub.fi/')
        count = 0
        cookies = {}
        while count < 60:
            count += 1
            time.sleep(1)
            if driver.current_url == 'https://oma.datahub.fi/#/':
                cookies = {c['name']: c['value'] for c in driver.get_cookies()}
                break
        if cookies=={}:
            raise Exception('Could not get cookies')
        with open("cookies.json", 'w') as f:
            json.dump(cookies, f)
        return cookies
    else:
        try:
            with open(file) as f:
                cookies = json.load(f)
        except:
            cookies = get_cookies() 
        return cookies  
def get_session(c: dict)->requests.Session:
    """Login to the Fingrid datahub API with cookies and return a session object

    Arguments:
        t -- The token

    Returns:
        requests.Session -- Session object
    """
    s = requests.Session()
    s.cookies.update(c)
    s.headers.update({'Authorization': 'Bearer ' + json.loads(urllib.parse.unquote(c['cap-user']))['token']})
    return s
def get_metering_points(s : requests.Session)->list:
    """Get metering points from the Fingrid Datahub API

    Arguments:
        s {requests.Session} -- Session object

    Returns:
        list -- List of lists of (meteringPointEAN, address)
    """
    r = s.get('https://oma.datahub.fi/_api/GetAgreementData?agreementStatus=CFD').json()
    return [(a['accountingPoint']['meteringPointEAN'],
        " ".join([a['accountingPoint']['meteringPointAddresses'][0][key] for key in ['streetName',
        'buildingNumber','stairwellIdentification','apartment']])) for a in r if '11' == a['agreementType']]
def get_consumption_data(s : requests.Session, meteringPointEAN : str, start : str, end : str)->list:
    """Get data from the Fingrid Datahub API

    Arguments:
        s {requests.Session} -- Session object
        meteringPointEAN {str} -- Metering point EAN
        start {str} -- Start date in format YYYY-MM-DDT00:00 (UTC)
        end {str} -- End date in format YYYY-MM-DDT00:00 (UTC)
    
    Returns:
        list -- List of lists of (timestamp (ISO 8601), consumption (kWh))       
    """
    r = s.get('https://oma.datahub.fi/_api/GetConsumptionData?meteringPointEAN=' + meteringPointEAN + \
    '&periodStartTS=' + start + ':00.000Z&periodEndTS=' + end + \
    ':00.000Z&unitType=kWh&productType=8716867000030&settlementRelevant=false&readingType=BN01').json()
    return [[(o['PeriodStartTime'],float(o['Quantity'])) for o in ts['Observations'] if o['Quality']=='OK'] for ts in r['TimeSeries']][0]
def logout(s : requests.Session)->bool:
    """Logout from the API
    
    Arguments:
        s {requests.Session} -- Session object

    Returns:
        bool -- True if logout was successful
    """
    return s.get('https://oma.datahub.fi/_api/logout').ok