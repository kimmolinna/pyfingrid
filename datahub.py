import pyfingrid as fg

cookies = fg.get_cookies()
print(cookies)
session = fg.get_session(cookies)
token = fg.get_token(cookies)
print(fg.get_metering_points(session,token))
print(fg.logout(session))