# %% [markdown]
# # Script 1: Initial mass data load (FARS 2016-2023)
#
# Runs the same person -> vehicle -> accident join as `load_fars_year.ipynb`, once for
# every year in `YEARS`, and saves one person-level table per year to
# `processed/preprocessed/fars_<YEAR>_person.<SAVE_FORMAT>`.
#
# Nothing is dropped, encoded, or changed here. Run once; scripts 2 and 3 read the output.
#
# Expected raw layout (unzipped NHTSA national CSV archives):
#     project/data/FARS2016NationalCSV/{accident,vehicle,person}.csv
#     ...
#     project/data/FARS2023NationalCSV/...
#
# Run from anywhere, e.g. the repo root:  python project/scripts/init_load.py
# (The `# %%` markers also let you run it cell by cell in VS Code / Jupyter.)

# %%
from pathlib import Path
import pandas as pd

YEARS = range(2016, 2024)   # 2016-2023 inclusive
SAVE_FORMAT = "parquet"         # "csv" (~300 MB/year) or "parquet" (~20 MB/year, needs pyarrow)

# Paths are anchored to this file (project/scripts/), so outputs land in project/
# no matter which directory the script is run from.
try:
    PROJECT_DIR = Path(__file__).resolve().parent.parent
except NameError:  # running cell by cell in Jupyter / VS Code, where __file__ is undefined
    PROJECT_DIR = next(p for p in (Path.cwd(), Path.cwd().parent, Path.cwd() / "project")
                       if (p / "scripts" / "init_load.py").exists())
DATA_DIR = PROJECT_DIR / "data"
OUT_DIR = PROJECT_DIR / "processed" / "preprocessed"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def find_file(folder, name):
    """Return the file in `folder` whose name matches `name`, ignoring case
    (2016 uses Person.CSV, later years use person.csv)."""
    for f in folder.iterdir():
        if f.name.lower() == name.lower():
            return f
    raise FileNotFoundError(f"{name} not found in {folder}")


def load_year(year):
    """Join vehicle and accident details onto each person for one year."""
    year_dir = DATA_DIR / f"FARS{year}NationalCSV"
    read = lambda name: pd.read_csv(find_file(year_dir, name), encoding="latin-1", low_memory=False)
    accident, vehicle, person = read("accident.csv"), read("vehicle.csv"), read("person.csv")

    df = person.merge(vehicle, on=["ST_CASE", "VEH_NO"], how="left",
                      suffixes=("", "_VEH"), validate="many_to_one")
    df = df.merge(accident, on="ST_CASE", how="left",
                  suffixes=("", "_ACC"), validate="many_to_one")

    # Same checks as load_fars_year.ipynb
    assert len(df) == len(person), "Row count changed during merge"
    assert df.shape[1] == person.shape[1] + (vehicle.shape[1] - 2) + (accident.shape[1] - 1)
    assert not df.duplicated(["ST_CASE", "VEH_NO", "PER_NO"]).any(), "Duplicate person keys"

    # Older person files may lack YEAR; add it so multi-year work can tell rows apart.
    if "YEAR" not in df:
        df["YEAR"] = year
    return df, {"year": year, "crashes": len(accident), "vehicles": len(vehicle),
                "people": len(df), "columns": df.shape[1]}


# %%
summary = []
for year in YEARS:
    year_dir = DATA_DIR / f"FARS{year}NationalCSV"
    if not year_dir.exists():
        print(f"{year}: SKIPPED, {year_dir} not found")
        summary.append({"year": year, "status": "missing raw folder"})
        continue
    df, info = load_year(year)
    out_path = OUT_DIR / f"fars_{year}_person.{SAVE_FORMAT}"
    if SAVE_FORMAT == "parquet":
        df.to_parquet(out_path, index=False)
    elif SAVE_FORMAT == "csv":
        df.to_csv(out_path, index=False)
    else:
        raise ValueError('SAVE_FORMAT must be "parquet" or "csv"')
    info.update(status="saved", file=out_path.name, MB=round(out_path.stat().st_size / 1e6))
    summary.append(info)
    print(f"{year}: {info['people']:,} people x {info['columns']} columns -> {out_path.name}")
    del df  # free memory before the next year

summary = pd.DataFrame(summary).set_index("year")
summary.to_csv(OUT_DIR / "load_summary.csv")
print()
print(summary.to_string())