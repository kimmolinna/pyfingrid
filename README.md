# pyfingrid
Fingrid Datahub API for Python

The code uses the [Selenium](https://selenium-python.readthedocs.io/) library and the [requests](https://pypi.org/project/requests/) to scrape the data from the [Fingrid Datahub](https://data.fingrid.fi/). Selenium is used to get cookies for the session.

## Usage

```python
cookies = get_cookies()                             # get_cookies() gets cookies with Selenium
or 
cookies = get_cookies("cookies.json")               # get cookies from a file
session = get_session()
cookies_to_session(session, cookies)
customerData = get_customer_data(session)
meteringPoints = get_metering_points(session)
data = get_consumption_data(session, meteringPoint, start, end)
ok = logout(session)
```

## Example

[datahub.py](./datahub.py) contains an example of how to use the functions.