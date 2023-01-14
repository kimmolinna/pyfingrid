import constant
import pyfingrid as fg
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filename=constant.LOGFILE,
    filemode='a')

logging.info('Starting to fetch power consumption data from Fingrid Datahub...')

metering_point = constant.ETERING_POINT
period_start = fg.prepare_start_time(1)
period_end = fg.prepare_end_time(1)

try:
    cookies = fg.get_cookies_from_file(constant.SESSIONFILE)
    session = fg.get_session(cookies)
    points = fg.get_consumption_data(metering_point, period_start, period_end, session)
except:
    logging.exception('Unable to read consumption from Datahub!')
    sys.exit()

for point in points:
    # Save the values where you want, this example simply prints the consumption.
    print(point['timestamp'] + ": " + str(point['consumption']) + " kWh")

logging.info(str(len(points)) + ' consumption points feteched from Datahub.')
