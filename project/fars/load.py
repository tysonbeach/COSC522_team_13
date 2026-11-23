"""Stage 2: join Person -> Vehicle -> Accident into one person-level table per year.

Nothing is dropped, encoded or changed here; the output is the raw join, saved as
processed/joined/fars_<YEAR>_person.parquet.
"""

import pandas as pd

from .config import JOINED_DIR
from .paths import joined_path, raw_dir


def find_file(folder, name):
    """The file in `folder` named `name`, ignoring case (2016 uses Person.CSV)."""
    for f in folder.iterdir():
        if f.name.lower() == name.lower():
            return f
    raise FileNotFoundError(f"{name} not found in {folder}")


def read_table(year, name):
    return pd.read_csv(find_file(raw_dir(year), name), encoding="latin-1", low_memory=False)


def join_year(year):
    """Each person with their vehicle's and crash's columns attached."""
    accident = read_table(year, "accident.csv")
    vehicle = read_table(year, "vehicle.csv")
    person = read_table(year, "person.csv")

    df = person.merge(
        vehicle,
        on=["ST_CASE", "VEH_NO"],
        how="left",
        suffixes=("", "_VEH"),
        validate="many_to_one",
    )
    df = df.merge(accident, on="ST_CASE", how="left", suffixes=("", "_ACC"), validate="many_to_one")

    assert len(df) == len(person), "Row count changed during merge"
    assert df.shape[1] == person.shape[1] + (vehicle.shape[1] - 2) + (accident.shape[1] - 1)
    assert not df.duplicated(["ST_CASE", "VEH_NO", "PER_NO"]).any(), "Duplicate person keys"

    if "YEAR" not in df:  # older person files lack YEAR
        df["YEAR"] = year
    counts = {"crashes": len(accident), "vehicles": len(vehicle), "people": len(df)}
    return df, counts


def main(years):
    JOINED_DIR.mkdir(parents=True, exist_ok=True)
    summary = []
    for year in years:
        if not raw_dir(year).exists():
            print(f"{year}: SKIPPED, {raw_dir(year)} not found (run 01_download.py)")
            summary.append({"year": year, "status": "missing raw folder"})
            continue
        df, counts = join_year(year)
        out_path = joined_path(year)
        df.to_parquet(out_path, index=False)
        summary.append(
            {
                "year": year,
                **counts,
                "columns": df.shape[1],
                "status": "saved",
                "file": out_path.name,
                "MB": round(out_path.stat().st_size / 1e6),
            }
        )
        print(f"{year}: {len(df):,} people x {df.shape[1]} columns -> {out_path.name}")

    # Update only the rows for the years just run, keeping the other years' rows.
    summary = pd.DataFrame(summary).set_index("year")
    summary_path = JOINED_DIR / "load_summary.csv"
    if summary_path.exists():
        previous = pd.read_csv(summary_path, index_col="year")
        summary = pd.concat([previous.drop(index=summary.index, errors="ignore"), summary])
    summary = summary.sort_index()
    summary.to_csv(summary_path)
    print("\n" + summary.to_string())
