import pyfingrid as fg
import pandas as pd
import awswrangler as wr
import sys
import datetime as dt

if len(sys.argv) < 2:
    year = dt.datetime.now().year
else:
    year = int(sys.argv[1])
cookies = fg.get_cookies("cookies.json")
session = fg.get_session()
fg.cookies_to_session(session, cookies)
customerData = fg.get_customer_data(session)
meteringPoints = fg.get_metering_points(session)
data = fg.get_consumption_data(session, meteringPoints[3][0], str(year-1)+'-12-31T22:00', str(year)+'-12-31T22:00')
df = pd.DataFrame(data,columns=['timestamp','consumption'])
df['timestamp'] = pd.to_datetime(df['timestamp'])
add = meteringPoints[3][1]
[add := add.replace(a,b) for a,b in [(' ',''),('.','')]]
wr.s3.to_parquet(df, "s3://linna/fingrid/"+add+"_"+ str(year) +".parquet")
fg.logout(session)