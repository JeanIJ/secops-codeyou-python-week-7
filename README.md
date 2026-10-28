# Code:You Week 7 — CMDB API Audit

A Python program that pulls asset inventory from a CMDB API, models each asset as an object, classifies risk, and writes a security-focused summary report.

Built for Code:You SecOps Python Assignment 7.

## Status

Assignment complete. `cmdb_api_audit.py` fetches the Ironclad CMDB sample, classifies each asset, prints the findings, and writes `cmdb_summary.txt`. Challenges A through D (error handling, high-priority review, top owner teams, and last-seen age) are implemented. Pagination is not handled; the reflection notes that as a follow-up for larger inventories.

The committed `cmdb_summary.txt` is a snapshot from one successful run (HTTP 200, 300 assets). Counts in that file match the sample below. Days since last seen depend on the date you run the script.

## Tech

- Python 3
- [`requests`](https://pypi.org/project/requests/) for the HTTP GET
- Standard library `datetime` for last-seen age

Risk rules in `Asset.risk_level()`:

- **HIGH** — internet exposed and criticality is high
- **MEDIUM** — internet exposed or criticality is high
- **LOW** — otherwise

High-priority review is production assets that are internet exposed or marked high criticality. An asset is stale when `last_seen` parses as `MM/DD/YYYY` and is 30 or more days ago.

## Setup

Install `requests` once:

```bash
python3 -m pip install requests
```

Set the Mockaroo API key in your environment. Replace the placeholder with your own key. Do not commit a real key:

```bash
export MOCKAROO_API_KEY="your-api-key-here"
```

The script calls `https://my.api.mockaroo.com/ironclad/cmdb.json` with an `X-API-Key` header taken from `MOCKAROO_API_KEY` and a 10 second timeout. If `MOCKAROO_API_KEY` is missing or blank, the script prints an error and exits before calling the API. Network errors, timeouts, non-success HTTP status, invalid JSON, and an unexpected response shape stop the script with a message.

## Usage

```bash
export MOCKAROO_API_KEY="your-api-key-here"
python3 cmdb_api_audit.py
```

The script prints status, asset counts, environment and risk breakdowns, internet-exposed assets, the high-priority production review, the top 3 owner teams by HIGH risk, and assets not seen in 30 or more days. It writes the same findings to `cmdb_summary.txt` in the working directory.

## What It Does

1. Sends a request to a CMDB API endpoint using an API key
2. Parses the JSON response into Python structures
3. Models each asset using a class with properties like hostname, environment, and criticality
4. Calculates a risk level for each asset based on internet exposure and criticality
5. Counts assets by environment and risk level
6. Identifies internet-exposed assets and high-priority production assets
7. Finds the top 3 owner teams with the most HIGH risk assets
8. Calculates how many days since each asset was last seen and flags stale assets
9. Writes all findings to a report file

## Files

- `cmdb_api_audit.py` — main script
- `cmdb_summary.txt` — report from a previous run (overwritten on the next run)

## Sample Output

```text
Status code: 200
Type of data: <class 'list'>
Number of assets: 300
Fields available: ['asset_id', 'hostname', 'asset_type', 'os', 'environment', 'owner_team', 'internet_exposed', 'criticality', 'last_seen']

First asset object:
db-3 (server, Windows, staging) owner=HR exposed=True crit=low last_seen=1/19/2025 risk=MEDIUM

=== Assets by Environment ===
staging 108
prod 101
dev 91

=== Assets by Risk Level ===
HIGH 54
MEDIUM 133
LOW 113

=== Internet-Exposed Assets ===
db-3 | owner=HR | crit=low | env=staging
...

=== High Priority Review (Prod + Exposed/Critical) ===
Count: 60
...

=== Top 3 Owner Teams by HIGH Risk ===
Executive Administration: 12
Engineering: 11
Finance: 9

=== Assets Not Seen in 30+ Days ===
Count: 300
...

Wrote report to cmdb_summary.txt
```

## Concepts Practiced

1. API requests: using the `requests` library to fetch data with headers and timeouts
2. JSON parsing: converting API responses into Python lists and dictionaries
3. Python classes and objects: the `Asset` class bundles data and behavior
4. `__init__`: constructor that initializes each asset from raw JSON
5. `__str__`: clean string representation for printing
6. Error handling: `try` and `except` for network and JSON failures
7. Conditionals: risk-level logic based on multiple factors
8. Dictionaries: counting and grouping assets by category
9. Sorting: ranking teams by high-risk asset count
10. `datetime`: parsing dates and calculating days since last seen
11. File I/O: writing the final report to a text file

## Challenges Completed

1. **A: Safer error handling.** Wraps API requests in `try` and `except` to catch connection errors, timeouts, and invalid JSON.
2. **B: High-priority review list.** Filters production assets that are internet exposed or marked high criticality.
3. **C: Top 3 owner teams by risk.** Counts HIGH risk assets per team, sorts descending, and reports the top 3.
4. **D: Last-seen age.** Parses dates with `datetime`, calculates days since last seen, and flags assets stale for 30 or more days.

## Reflection

Using a class made it easier to bundle each asset's data and behavior together, so I could call `asset.risk_level()` instead of writing separate functions for every asset. The hardest part was understanding how `datetime.strptime` parses the `MM/DD/YYYY` format for the last-seen calculation. To make this better, I would add pagination handling if the API returns more than one page of results, since real CMDBs often contain thousands of assets.
