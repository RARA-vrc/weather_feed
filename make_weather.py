"""room1206's weather feed: the latest AMeDAS air temperatures of 16 Japanese cities, as one small JSON file for the
world's thermometer (Room1206Climate.weatherUrl). Run by .github/workflows/weather.yml every 10 minutes; it writes
docs/room1206_weather.json, which GitHub Pages serves (*.github.io is on VRChat's trusted list for String Loading, so
players need no "Allow Untrusted URLs").

Source: 気象庁ホームページ (Japan Meteorological Agency), AMeDAS. The world shows 「気象庁」 next to the reading.
Two small requests a run: data/latest_time.txt and that time's data/map/YYYYMMDDHHMM00.json.

Usage: python make_weather.py [out_path]   (default docs/room1206_weather.json next to this file)
"""
import json
import os
import sys
import urllib.request
from datetime import datetime

BASE = "https://www.jma.go.jp/bosai/amedas/data/"
# Room1206Climate's cities (the same order there), with their AMeDAS station numbers (const/amedastable.json)
CITIES = [
    ("tokyo", "44132"), ("sapporo", "14163"), ("kushiro", "19432"), ("aomori", "31312"), ("akita", "32402"),
    ("morioka", "33431"), ("yamagata", "35426"), ("sendai", "34392"), ("niigata", "54232"), ("nagoya", "51106"),
    ("osaka", "62078"), ("hiroshima", "67437"), ("kochi", "74182"), ("fukuoka", "82182"), ("kagoshima", "88317"),
    ("naha", "91197"),
]


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "room1206-weather-feed"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "docs", "room1206_weather.json")
    latest = get(BASE + "latest_time.txt").strip()                 # e.g. 2026-11-05T15:20:00+09:00
    t = datetime.fromisoformat(latest)
    data = json.loads(get(BASE + "map/" + t.strftime("%Y%m%d%H%M00") + ".json"))
    temps = {}
    for key, sid in CITIES:
        v = data.get(sid, {}).get("temp")
        temps[key] = v[0] if isinstance(v, list) and v and isinstance(v[0], (int, float)) and (len(v) < 2 or v[1] == 0) else None
    if all(v is None for v in temps.values()):
        sys.exit("no readings")
    feed = {
        "source": "気象庁 アメダス / JMA AMeDAS",
        "time": latest,
        "hour": round(t.hour + t.minute / 60, 3),                 # Japan's time of the reading
        "t": temps,
    }
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(feed, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")
    print(latest, sum(v is not None for v in temps.values()), "cities ->", out)


if __name__ == "__main__":
    main()
