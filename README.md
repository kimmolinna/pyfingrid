# pyfingrid
Fingrid Datahub API for Python

At the moment this is a proof of concept. The API is not yet complete and the code is not yet documented.
The code uses the [Selenium](https://selenium-python.readthedocs.io/) library and the [requests](https://pypi.org/project/requests/) to scrape the data from the [Fingrid Datahub](https://data.fingrid.fi/). Selenium is used until the authorization and after that requests is used with authorization Token.
In the future the data is then parsed and returned as a Pandas DataFrame.

## Usage
The code is not yet documented and the API is not yet complete. The code is not yet tested and the API is not yet stable.

```python
cookies = get_cookies()
session = get_session(cookies)
token = get_token(cookies)
print(get_metering_points(session,token))
ok = logout(session)
```