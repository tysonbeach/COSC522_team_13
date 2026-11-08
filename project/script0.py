# Script 0: download and unzip FARS national CSV archives into project/data/
# Run from project/ (or the repo root):  python script0_download_fars.py
# Re-running skips years that are already downloaded.
import shutil
import tempfile
import urllib.request
import zipfile
from pathlib import Path

YEARS = range(2016, 2024)  # 2016-2023
URL = "https://static.nhtsa.gov/nhtsa/downloads/FARS/{y}/National/FARS{y}NationalCSV.zip"

PROJECT_DIR = Path.cwd() if Path("load_fars_year.ipynb").exists() else Path.cwd() / "project"
DATA_DIR = PROJECT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

for y in YEARS:
    target = DATA_DIR / f"FARS{y}NationalCSV"
    if target.exists() and any(f.name.lower() == "person.csv" for f in target.iterdir()):
        print(f"{y}: already present, skipping")
        continue
    zip_path = DATA_DIR / f"FARS{y}NationalCSV.zip"
    print(f"{y}: downloading {URL.format(y=y)} ...")
    urllib.request.urlretrieve(URL.format(y=y), zip_path)

    # Some years' zips have a nested folder; find the folder that holds person.csv.
    with tempfile.TemporaryDirectory() as tmp:
        zipfile.ZipFile(zip_path).extractall(tmp)
        hits = [p.parent for p in Path(tmp).rglob("*") if p.name.lower() == "person.csv"]
        if not hits:
            raise FileNotFoundError(f"No person.csv inside {zip_path.name}")
        shutil.rmtree(target, ignore_errors=True)
        shutil.copytree(hits[0], target)
    zip_path.unlink()  # keep only the unzipped folder
    print(f"{y}: saved to {target.relative_to(PROJECT_DIR)}")

print("Done. Next: python script1_load_all_years.py")