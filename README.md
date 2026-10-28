# Code:You Week 7 — CMDB API Audit

This is my Week 7 script for Code:You SecOps Python. `cmdb_api_audit.py` pulls the Ironclad CMDB sample, makes an `Asset` for each record, gives it a risk level, prints the results, and writes `cmdb_summary.txt`.

The `cmdb_summary.txt` in the repo is from one run that returned HTTP 200 and 300 assets. The counts in the sample below match that file. How many days since last seen depends on the day you run the script.

## Setup

Python 3 and the `requests` library:

```bash
python3 -m pip install requests
```

The script reads the Mockaroo key from the environment. Put your own key in place of the placeholder, and keep the real key out of the repo.

```bash
export MOCKAROO_API_KEY="your-api-key-here"
```

It GETs `https://my.api.mockaroo.com/ironclad/cmdb.json`, sends that key in the `X-API-Key` header, and uses a 10 second timeout. If `MOCKAROO_API_KEY` is missing or blank, the script prints an error and exits before it calls the API. A network error, a timeout, a non-success status code, invalid JSON, or a response that is not a list of assets also stops the script and prints a message.

Risk in `Asset.risk_level()`:

- **HIGH**: internet exposed and criticality is high
- **MEDIUM**: internet exposed or criticality is high
- **LOW**: anything else

The high-priority review is production assets that are internet exposed or marked high criticality. An asset is stale when `last_seen` parses as `MM/DD/YYYY` and that date is 30 or more days ago. The age check uses `datetime` from the standard library.

## Usage

```bash
export MOCKAROO_API_KEY="your-api-key-here"
python3 cmdb_api_audit.py
```

The script prints the status code, the asset count, totals by environment and risk, the internet-exposed assets, the high-priority production review, the top 3 owner teams by HIGH risk, and assets not seen in 30 or more days. It writes the same findings to `cmdb_summary.txt` in the current directory. The next run overwrites that file.

- `cmdb_api_audit.py`: the script
- `cmdb_summary.txt`: the report from a previous run

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

## What I practiced

Calling an API with `requests` (headers and a timeout), reading the JSON into lists and dictionaries, an `Asset` class with `__init__` and `__str__`, `try` and `except` around the request, conditionals for the risk level, dictionaries to count and group assets, sorting owner teams by how many HIGH risk assets they have, `datetime` to parse last seen and count the days, and writing the report out to a text file.

## Challenges Completed

1. **A: Safer error handling.** The API request sits in `try` and `except` so connection errors, timeouts, and invalid JSON print a message and stop the script.
2. **B: High-priority review list.** Production assets that are internet exposed or marked high criticality.
3. **C: Top 3 owner teams by risk.** Counts HIGH risk assets per team, sorts that count from highest to lowest, and reports the top 3.
4. **D: Last-seen age.** Parses `last_seen` with `datetime`, calculates days since that date, and flags assets that are 30 or more days old.

## Reflection

Using a class made it easier to bundle each asset's data and behavior together, so I could call `asset.risk_level()` instead of writing separate functions for every asset. The hardest part was understanding how `datetime.strptime` parses the `MM/DD/YYYY` format for the last-seen calculation. To make this better, I would add pagination handling if the API returns more than one page of results, since real CMDBs often contain thousands of assets.
