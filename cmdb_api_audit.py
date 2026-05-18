import requests
from datetime import datetime

API_URL = "https://my.api.mockaroo.com/ironclad/cmdb.json"
HEADERS = {"X-API-Key": "cf7bbbd0"}

try:
    response = requests.get(API_URL, headers=HEADERS, timeout=10)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.RequestException as e:
    print("Network/Request failed:", e)
    raise SystemExit
except ValueError as e:
    print("Invalid JSON received:", e)
    raise SystemExit

print("Status code:", response.status_code)

print("Type of data:", type(data))

if isinstance(data, list) and data:
    print("Number of assets:", len(data))
    print("Fields available:", list(data[0].keys()))
    print("First asset preview:", data[0])
else:
    print("Unexpected JSON structure. Expected a list of assets.")
    raise SystemExit


class Asset:
    def __init__(self, raw: dict):
        self.raw = raw
        self.asset_id = raw.get("asset_id")
        self.hostname = raw.get("hostname", "unknown")
        self.asset_type = raw.get("asset_type", "unknown")
        self.os = raw.get("os", "unknown")
        self.environment = raw.get("environment", "unknown")
        self.owner_team = raw.get("owner_team", "unknown")
        self.internet_exposed = bool(raw.get("internet_exposed", False))
        self.criticality = raw.get("criticality", "low")
        self.last_seen = raw.get("last_seen", "unknown")

    def risk_level(self) -> str:
        crit_high = str(self.criticality).lower() == "high"
        if self.internet_exposed and crit_high:
            return "HIGH"
        if self.internet_exposed or crit_high:
            return "MEDIUM"
        return "LOW"

    def days_since_seen(self):
        try:
            seen = datetime.strptime(self.last_seen, "%m/%d/%Y")
            return (datetime.now() - seen).days
        except (ValueError, TypeError):
            return None

    def __str__(self) -> str:
        return (
            f"{self.hostname} ({self.asset_type}, {self.os}, {self.environment}) "
            f"owner={self.owner_team} exposed={self.internet_exposed} "
            f"crit={self.criticality} last_seen={self.last_seen} risk={self.risk_level()}"
        )


assets = []
for record in data:
    assets.append(Asset(record))

print()
print("First asset object:")
print(assets[0] if assets else "No assets")


env_counts = {}
for a in assets:
    env = a.environment
    env_counts[env] = env_counts.get(env, 0) + 1

print()
print("=== Assets by Environment ===")
for env, count in env_counts.items():
    print(env, count)

risk_counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
for a in assets:
    risk_counts[a.risk_level()] += 1

print()
print("=== Assets by Risk Level ===")
for k, v in risk_counts.items():
    print(k, v)

exposed = [a for a in assets if a.internet_exposed]

print()
print("=== Internet-Exposed Assets ===")
for a in exposed:
    print(f"{a.hostname} | owner={a.owner_team} | crit={a.criticality} | env={a.environment}")


high_priority = [
    a for a in assets
    if a.environment == "prod" and (a.internet_exposed or str(a.criticality).lower() == "high")
]

print()
print("=== High Priority Review (Prod + Exposed/Critical) ===")
print(f"Count: {len(high_priority)}")
for a in high_priority:
    print(f"- {a.hostname} | owner={a.owner_team} | crit={a.criticality} | exposed={a.internet_exposed}")


team_high_risk = {}
for a in assets:
    if a.risk_level() == "HIGH":
        team = a.owner_team
        team_high_risk[team] = team_high_risk.get(team, 0) + 1

top_teams = sorted(team_high_risk.items(), key=lambda x: x[1], reverse=True)[:3]

print()
print("=== Top 3 Owner Teams by HIGH Risk ===")
for team, count in top_teams:
    print(f"{team}: {count}")


stale_assets = [a for a in assets if a.days_since_seen() is not None and a.days_since_seen() >= 30]

print()
print("=== Assets Not Seen in 30+ Days ===")
print(f"Count: {len(stale_assets)}")
for a in stale_assets:
    print(f"- {a.hostname} | last_seen={a.last_seen} | days_ago={a.days_since_seen()}")


with open("cmdb_summary.txt", "w", encoding="utf-8") as out:
    print("Ironclad CMDB API Audit Report", file=out)
    print("==============================", file=out)
    print(f"URL: {API_URL}", file=out)
    print(f"Status: {response.status_code}", file=out)
    print(f"Total assets: {len(assets)}", file=out)
    print(file=out)

    print("Assets by Environment:", file=out)
    for env, count in env_counts.items():
        print(f"- {env}: {count}", file=out)

    print(file=out)
    print("Assets by Risk Level:", file=out)
    for level, count in risk_counts.items():
        print(f"- {level}: {count}", file=out)

    print(file=out)
    print("Internet-Exposed Assets:", file=out)
    for a in exposed:
        print(f"- {a.hostname} | owner={a.owner_team} | crit={a.criticality} | env={a.environment}", file=out)

    print(file=out)
    print("High Priority Review (Prod + Exposed/Critical):", file=out)
    print(f"Count: {len(high_priority)}", file=out)
    for a in high_priority:
        print(f"- {a.hostname} | owner={a.owner_team} | crit={a.criticality} | exposed={a.internet_exposed}", file=out)

    print(file=out)
    print("Top 3 Owner Teams by HIGH Risk:", file=out)
    for team, count in top_teams:
        print(f"- {team}: {count}", file=out)

    print(file=out)
    print("Assets Not Seen in 30+ Days:", file=out)
    print(f"Count: {len(stale_assets)}", file=out)
    for a in stale_assets:
        print(f"- {a.hostname} | last_seen={a.last_seen} | days_ago={a.days_since_seen()}", file=out)

print()
print("Wrote report to cmdb_summary.txt")