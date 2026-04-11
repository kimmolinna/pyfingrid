# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

`pyfingrid` is a Python library for accessing the [Fingrid Datahub](https://oma.datahub.fi/) API. It scrapes session cookies using Selenium/ChromeDriver, then makes authenticated REST requests to retrieve electricity metering data.

## Architecture

### `pyfingrid.py` — the library

The core module. All public functions follow this flow:

1. **Authentication**: `get_cookies()` opens Chrome via Selenium, waits for the user to log in, captures session cookies, and saves them to `cookies.json`. Alternatively reads cookies from a file.
2. **Session setup**: `get_session()` + `cookies_to_session(session, cookies)` — creates a `requests.Session`, applies cookies, and extracts the Bearer token from the `cap-user` cookie.
3. **Data retrieval**: `get_customer_data()`, `get_metering_points()`, `get_consumption_data()` — all call `get_response()` which auto-refreshes cookies on 401.
4. **Logout**: `logout(session)` hits the logout endpoint.

`get_metering_points()` filters for agreement type `'11'` (electricity consumption agreements) and returns `(meteringPointEAN, address)` tuples.

`get_consumption_data()` expects UTC timestamps in `YYYY-MM-DDT00:00` format and returns `(ISO 8601 timestamp, kWh float)` tuples for observations with `Quality=='OK'`.

### `datahub.py` — example script

Fetches a full year of consumption data for a specific metering point (hardcoded EAN `643003825102738370`) and writes it as Parquet to S3 (`s3://linna/fingrid/home_<year>.parquet`) using AWS Wrangler. Accepts an optional year argument: `python datahub.py 2024`.

Cloudflare R2 is available as an alternative backend — see the commented-out code using `boto3.Session(profile_name="cloudflare")` and `wr.config.s3_endpoint_url`.

## Dependencies

- `selenium`, `webdriver-manager` — browser automation for login
- `requests` — HTTP session
- `pandas`, `awswrangler` — data transformation and S3 upload (example script only)
- `keyring` — retrieves Cloudflare account ID from system keychain (example script only)

## Key details

- `cookies.json` is gitignored; it holds live session credentials.
- The Bearer token is URL-decoded from the `cap-user` cookie value (JSON field `token`).
- Date range for `get_consumption_data` should be expressed in UTC; Finnish local time is UTC+2 (summer UTC+3), so year boundaries shift accordingly (e.g., `2023-12-31T22:00` to `2024-12-31T22:00` for Finnish calendar year 2024).
