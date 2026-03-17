import csv
import json
from datetime import datetime, timedelta, timezone

start_year = 2025
end_year = 2026
start_month = 3
end_month = 2

HOURLY_FIELDS = [
    "temperature_2m: temperature",
    "precipitation_probability",
    "precipitation",
    "wind_speed_10m: wind_speed",
    "wind_gusts_10m: wind_gusts",
    "wind_direction_10m: wind_direction",
    "visibility",
    "weather_code",
]


# Parse "json_key: csv_name" or plain "field" entries
def _parse_field(f):
    if ": " in f:
        json_key, csv_name = f.split(": ", 1)
        return json_key.strip(), csv_name.strip()
    return f, f


HOURLY_FIELD_PAIRS = [_parse_field(f) for f in HOURLY_FIELDS]
CSV_COLUMNS = [csv_name for _, csv_name in HOURLY_FIELD_PAIRS]


def weather_csv():
    print("hello")
    with open("./data.csv", "w", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=["timestamp"] + CSV_COLUMNS)
        writer.writeheader()
        for y in range(start_year, end_year + 1):
            m_start = start_month if y == start_year else 1
            m_end = end_month if y == end_year else 12
            for m in range(m_start, m_end + 1):
                try:
                    with open(f"./data/weather/weather_{y}-{m:02d}.json") as f:
                        data = json.load(f)
                except FileNotFoundError:
                    continue
                t = datetime.fromtimestamp(data["hourly_time_start"], tz=timezone.utc)
                interval = timedelta(seconds=data["hourly_interval"])
                hourly = data["hourly"]
                first_json_key = HOURLY_FIELD_PAIRS[0][0]
                n = len(hourly[first_json_key])
                for i in range(n):
                    hour_t = t + i * interval
                    values = {}
                    for json_key, csv_name in HOURLY_FIELD_PAIRS:
                        v = hourly[json_key][i]
                        values[csv_name] = "" if v != v else "{:.3f}".format(v)
                    for minute in range(60):
                        row = {
                            "timestamp": (hour_t + timedelta(minutes=minute)).strftime(
                                "%Y-%m-%dT%H:%M"
                            )
                        }
                        row.update(values)
                        writer.writerow(row)


weather_csv()
