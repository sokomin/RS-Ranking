import argparse
import csv
import datetime as dt
import json
from pathlib import Path

import requests


BASE_URL = "https://lnk-rs-web-files.s3.ap-northeast-1.amazonaws.com"
SERVERS = [
    ("WORLD01", "strasserad"),
    ("WORLD02", "vaultish"),
    ("WORLD03", "bridgehead"),
    ("WORLD04", "gold"),
]


def ymd_range(start, end):
    cur = dt.datetime.strptime(start, "%Y%m%d").date()
    last = dt.datetime.strptime(end, "%Y%m%d").date()
    while cur <= last:
        yield cur.strftime("%Y%m%d")
        cur += dt.timedelta(days=1)


def parse_ymd(value):
    return dt.datetime.strptime(value, "%Y%m%d").date()


def existing_dates():
    dates = []
    for directory in (Path("out/jpn_lv"), Path("out/jpn_gh")):
        if not directory.exists():
            continue
        for path in directory.iterdir():
            prefix = path.name[:8]
            if len(prefix) == 8 and prefix.isdigit():
                dates.append(parse_ymd(prefix))
    return dates


def resolve_range(args):
    end = parse_ymd(args.end) if args.end else dt.date.today() - dt.timedelta(days=1)
    if args.start:
        start = parse_ymd(args.start)
    else:
        dates = existing_dates()
        start = max(dates) + dt.timedelta(days=1) if dates else end
    return start, end


def fetch_json(session, date, world, name):
    url = f"{BASE_URL}/meta/ranks/{date}/{world}/{name}.json"
    res = session.get(url, timeout=20)
    if res.status_code in (403, 404):
        return []
    res.raise_for_status()
    return json.loads(res.content.decode("utf-8"))


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerows(rows)


def write_level(session, date, world, server):
    data = fetch_json(session, date, world, "rebirth")
    if not data:
        return None, 0

    rows = [["", "-", "職業", "キャラクター", "レベル", "転生回数"]]
    for rank, rec in enumerate(data, 1):
        rows.append([
            rank,
            "-",
            "",
            rec.get("name", ""),
            rec.get("lev", ""),
            rec.get("rebirthcount", ""),
        ])
    path = Path("out/jpn_lv") / f"{date}_{server}_0.csv"
    write_csv(path, rows if len(rows) > 1 else [])
    return path, max(0, len(rows) - 1)


def write_gh(session, date):
    castle_by_server = {}
    for world, server in SERVERS:
        castle_by_server[server] = fetch_json(session, date, world, "castle")
    if not any(castle_by_server.values()):
        return 0

    total = 0
    for server, data in castle_by_server.items():
        if not data:
            continue

        rows_3 = []
        rows_1 = []
        for rank, rec in enumerate(data, 1):
            row = [
                f"{rank}位",
                "",
                rec.get("strName", ""),
                rec.get("strMaster", ""),
                rec.get("iLevel", ""),
                rec.get("iHallLevel", ""),
            ]
            hall_level = rec.get("iHallLevel")
            if hall_level in (3, 4):
                rows_3.append(row)
            elif hall_level in (1, 2):
                rows_1.append(row)
        path_3 = Path("out/jpn_gh") / f"{date}_{server}_3.csv"
        path_1 = Path("out/jpn_gh") / f"{date}_{server}_1.csv"
        write_csv(path_3, rows_3)
        write_csv(path_1, rows_1)
        total += len(rows_3) + len(rows_1)

    rows_5 = []
    for server in ("strasserad", "vaultish", "bridgehead", "gold"):
        recs = [rec for rec in castle_by_server[server] if rec.get("iHallLevel") == 5]
        if not recs:
            rows_5.append(["", "", "", "", "", ""])
            continue
        rec = recs[0]
        rows_5.append([
            "1位",
            "",
            rec.get("strName", ""),
            rec.get("strMaster", ""),
            rec.get("iLevel", ""),
            rec.get("iHallLevel", ""),
        ])
    write_csv(Path("out/jpn_gh") / f"{date}_strasserad_5.csv", rows_5)
    return total + len([row for row in rows_5 if row[2]])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start")
    parser.add_argument("--end")
    args = parser.parse_args()

    start, end = resolve_range(args)
    if start > end:
        print(f"up to date: latest local data is {start - dt.timedelta(days=1):%Y%m%d}")
        return

    with requests.Session() as session:
        print(f"fetch range: {start:%Y%m%d}..{end:%Y%m%d}")
        for date in ymd_range(start.strftime("%Y%m%d"), end.strftime("%Y%m%d")):
            for world, server in SERVERS:
                path, count = write_level(session, date, world, server)
                if path:
                    print(f"level {date} {server}: {count} rows -> {path}")
                else:
                    print(f"level {date} {server}: skipped")
            gh_count = write_gh(session, date)
            print(f"gh {date}: {gh_count} rows")


if __name__ == "__main__":
    main()
