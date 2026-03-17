"""
Downloader for monthly 511 historical datafeeds (zipped GTFS bundles).

Given a period [start, end] inclusive (by month), this script downloads
`511_data_YYYY-MM.zip` files to a target directory (default: `trial`).
"""

import os
import zipfile
from datetime import datetime

import requests
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv


def get_datafeeds(
    api_key, operator_id, period_start, period_end, output_dir, unzip_dir=None
):
    """Download monthly 511 datafeed archives for a given operator.

    Parameters:
    - api_key: str – 511 API key.
    - operator_id: str – Agency/operator code (e.g., 'CT' for Caltrain).
    - period_start: datetime – Inclusive start (only year/month used).
    - period_end: datetime – Inclusive end (only year/month used).
    - output_dir: str – Directory to save `511_data_YYYY-MM.zip` files.

    Notes:
    - The endpoint expects the `historic` query param in 'YYYY-MM' format.
    - HTTP failures are logged; successful responses are written to disk.
    - If unzip_dir is provided, each zip is extracted to unzip_dir/YYYY-MM/.
    """
    os.makedirs(output_dir, exist_ok=True)
    if unzip_dir:
        os.makedirs(unzip_dir, exist_ok=True)
    current = period_start
    while current <= period_end:
        ym = current.strftime("%Y-%m")
        fname = f"511_data_{ym}.zip"
        url = f"http://api.511.org/transit/datafeeds?api_key={api_key}&operator_id={operator_id}&historic={ym}"
        path = os.path.join(output_dir, fname)
        print(f"Downloading: {url}")
        resp = requests.get(url)
        if resp.ok:
            with open(path, "wb") as f:
                f.write(resp.content)
            print(f"Saved {fname}")
            if unzip_dir:
                dest = os.path.join(unzip_dir, ym)
                os.makedirs(dest, exist_ok=True)
                with zipfile.ZipFile(path) as zf:
                    zf.extractall(dest)
                print(f"Extracted to {dest}")
        else:
            print(f"Failed for {ym}: {resp.status_code}")
        current += relativedelta(months=1)


if __name__ == "__main__":
    load_dotenv()
    api_key = os.environ["GTFS_TOKEN"]
    operator_id = "CT"
    period_start = datetime(2025, 3, 1)
    period_end = datetime(2026, 2, 28)
    output_dir = "data/gtfs"
    unzip_dir = "data/gtfs_unzipped"
    get_datafeeds(api_key, operator_id, period_start, period_end, output_dir, unzip_dir)
