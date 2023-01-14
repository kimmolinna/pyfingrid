import json
import pyfingrid as fg

# Open Chrome for strong authentication. Save cookies to a textfile for later usage.
cookies = fg.get_cookies()
f = open("session.txt", "w")
f.write(json.dumps(cookies))
f.close()

# Print metering point information.
session = fg.get_session(cookies)
agreements = json.loads(fg.get_agreements(session))
for agreement in agreements:
    print("agreementIdentification: " + str(agreement['agreementIdentification']))
    print("meteringPointEAN: " + str(agreement['accountingPoint']['meteringPointEAN']))

# If you want to log out and end the session you just stored to the textfile, uncomment this.
# print(fg.logout(session))
