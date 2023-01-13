import pyfingrid as fg

cookies = fg.get_cookies()
session = fg.get_session(cookies)
print(fg.get_metering_points(session))
print(fg.logout(session))