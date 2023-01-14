from datetime import date, datetime, timedelta
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import json,requests,time
import urllib.parse
import pytz

def get_cookies():
    """Get cookies from the Fingrid datahub API

    Raises:
        Exception: If login is not successful in 60 seconds

    Returns:
        dict -- Cookies
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

def get_session(c: dict):
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

def get_cookies_from_file(filename: str):
    """Reads cookies from given file.

    Arguments:
        filename -- full path to the file containinig the session variables.

    Returns:
        dict -- Variables of the Datahub cookie.
    """
    try:
        f = open(filename)
        cookies = json.loads(f.readline())
        f.close()
    except:
        raise Exception("Unable to open session file or invalid file content!")

    return cookies


def get_metering_points(s : requests.Session):
    """Get metering points from the Fingrid Datahub API

    Arguments:
        s {requests.Session} -- Session object
    """
    r = s.get('https://oma.datahub.fi/_api/GetAgreementData?agreementStatus=CFD')
    return r.content

def get_consumption_data(metering_point: str, period_start: str, period_end: str, s : requests.Session):
    """Get consumption data from the API

    Arguments:
        metering_point {str} -- Metering point ID
        period_start {str} -- Date and time in UTC, in ISO8601 format
        periond_end {str} -- Date and time in UTC, in ISO8601 format
        s {requests.Session} -- Session object
    """
    r = s.get('https://oma.datahub.fi/_api/GetConsumptionData?meteringPointEAN=' + metering_point + '&periodStartTS=' + period_start + '&periodEndTS=' + period_end + '&unitType=kWh&productType=8716867000030&settlementRelevant=false&readingType=BN01')

    if r.status_code == 401:
        raise Exception("HTTP 401: Access denied, session is not valid.")
    elif r.status_code != 200:
        raise Exception("Unexpected response from Datahub API: " + r.status_code)

    points = []

    try:
        j = json.loads(r.content)
        items = j['TimeSeries'][0]['Observations']
    except:
        return points

    for item in items:
        point = { "timestamp": item['PeriodStartTime'], "consumption": float(item['Quantity'])}
        points.append(point)

    return points

def logout(s : requests.Session):
    """Logout from the API
    
    Arguments:
        s {requests.Session} -- Session object
    """
    r = s.get('https://oma.datahub.fi/_api/logout')
    return r.ok

def prepare_start_time(delta: int):
    """Prepare the start time for the consumption query.

    Arguments:
        delta {int} -- Number of days in history.

    Returns:
        str -- Date and time in UTC, in the ISO8601 format the API expects.
    """
    # Prepare datetime object on local timezone, with time part at 00:00
    d = datetime.combine((date.today() - timedelta(days=delta)), datetime.min.time())
    # Convert from local timezone to UTC and format to expected ISO8601 format.
    utc = d.astimezone(pytz.utc).isoformat('T', 'milliseconds').replace('+00:00', 'Z')
    return utc

def prepare_end_time(delta: int):
    """Prepare the end time for the consumption query.

    Arguments:
        delta {int} -- Number of days in history.

    Returns:
        str -- Date and time in UTC, in the ISO8601 format the API expects.
    """
    # Prepare datetime object on local timezone, with time part at 23:59
    d = datetime.combine((date.today() - timedelta(days=delta)), datetime.max.time())
    # Convert from local timezone to UTC and format to expected ISO8601 format.
    utc = d.astimezone(pytz.utc).isoformat('T', 'milliseconds').replace('+00:00', 'Z')
    return utc
