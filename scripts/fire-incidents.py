import os

import requests

os.makedirs("data/raw", exist_ok=True)

url = "https://incidents.fire.ca.gov/imapdata/mapdataall.csv"
dest = "data/raw/cal-fire-incident.csv"

response = requests.get(url, timeout=60)
response.raise_for_status()

with open(dest, "wb") as f:
    f.write(response.content)

print(f"Saved {len(response.content) / 1024:.1f} KB to {dest}")
