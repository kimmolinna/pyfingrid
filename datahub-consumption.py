import constant
import pyfingrid as fg
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filename=constant.LOGFILE,
    filemode='a')

def get_cookies_from_file():
    """Reads cookies from session.txt
    
    Returns:
        dict -- Variables of the Datahub cookie.
    """
    try:
        f = open(constant.SESSIONFILE)
        cookies = json.loads(f.readline())
        f.close()
    except:
        logging.exception("Unable to open session file or invalid file content!")
        raise

    return cookies

if __name__ == '__main__':
    logging.info('Starting to fetch power consumption data from Fingrid Datahub...')

    cookies = get_cookies_from_file()
    session = fg.get_session(cookies)

    metering_point = constant.METERING_POINT
    period_start = fg.prepare_start_time(1)
    period_end = fg.prepare_end_time(1)

    try:
        response = fg.get_consumption_data(metering_point, period_start, period_end, session)
    except:
        logging.exception('Unexpected response from Datahub API!')
        raise

    try:
        consumption = json.loads(response)
        items = consumption['TimeSeries'][0]['Observations']
    except:
        logging.info('No consumption data available for the selected time range.')
        raise

    for item in items:
        timestamp = item['PeriodStartTime']
        value = float(item['Quantity'])
        # Save the values where you want, this example simply prints the consumption.
        print(timestamp + ": " + str(value) + " kWh")
        
    logging.info('Consumption successfully fetched from Datahub!')
