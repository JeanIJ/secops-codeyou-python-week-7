# CMDB API Audit

A Python program that pulls asset inventory data from an API, models each asset as an object, classifies risk, and produces a security focused summary report.

Built for Code:You SecOps Python Assignment 7.

## What It Does

1. Sends a request to a CMDB API endpoint using an API key
2. Parses the JSON response into Python structures
3. Models each asset using a class with properties like hostname, environment, and criticality
4. Calculates a risk level for each asset based on internet exposure and criticality
5. Counts assets by environment and risk level
6. Identifies internet exposed assets and high priority production assets
7. Finds the top 3 owner teams with the most HIGH risk assets
8. Calculates how many days since each asset was last seen and flags stale assets
9. Writes all findings to a report file

## Files

1. cmdb_api_audit.py: Main script
2. cmdb_summary.txt: Output report generated automatically

## How to Run

Install the requests library one time:

    python3 -m pip install requests

Run the script:

    python3 cmdb_api_audit.py

## Sample Output

    Status code: 200
    Type of data: &lt;class 'list'&gt;
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

## Concepts Practiced

1. API Requests: using the requests library to fetch data with headers and timeouts
2. JSON Parsing: converting API responses into Python lists and dictionaries
3. Python Classes and Objects: Asset class bundles data and behavior
4. __init__: constructor that initializes each asset from raw JSON
5. __str__: clean string representation for printing
6. Error Handling: try and except blocks for network and JSON failures
7. Conditionals: risk level logic based on multiple factors
8. Dictionaries: counting and grouping assets by category
9. Sorting: ranking teams by high risk asset count
10. datetime: parsing dates and calculating days since last seen
11. File I/O: writing the final report to a text file

## Challenges Completed

1. A: Safer Error Handling. Wraps API requests in try and except to catch connection errors, timeouts, and invalid JSON.
2. B: High Priority Review List. Filters production assets that are internet exposed or marked high criticality.
3. C: Top 3 Owner Teams by Risk. Counts HIGH risk assets per team, sorts descending, and reports the top 3.
4. D: Last Seen Age. Parses dates with datetime, calculates days since last seen, and flags assets stale for 30 or more days.

## Reflection

Using a class made it easier to bundle each asset's data and behavior together, so I could call asset.risk_level() instead of writing separate functions for every asset. The hardest part was understanding how datetime.strptime parses the MM/DD/YYYY format for the last seen calculation. To make this better, I would add pagination handling if the API returns more than one page of results, since real CMDBs often contain thousands of assets.