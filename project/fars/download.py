"""Stage 1: download and unzip the FARS national CSV archives into project/data/."""

import shutil
import tempfile
import urllib.request
import zipfile
from pathlib import Path

from .config import DATA_DIR, PROJECT_DIR
from .paths import raw_dir

URL = "https://static.nhtsa.gov/nhtsa/downloads/FARS/{y}/National/FARS{y}NationalCSV.zip"


def has_person_file(folder):
    return folder.exists() and any(f.name.lower() == "person.csv" for f in folder.iterdir())


def download_year(year):
    """Download one year's archive and keep only the folder that holds person.csv."""
    target = raw_dir(year)
    if has_person_file(target):
        print(f"{year}: already present, skipping")
        return
    DATA_DIR.mkdir(exist_ok=True)
    zip_path = DATA_DIR / f"FARS{year}NationalCSV.zip"
    print(f"{year}: downloading {URL.format(y=year)} ...")
    urllib.request.urlretrieve(URL.format(y=year), zip_path)

    # Some years' zips have a nested folder; find the folder that holds person.csv.
    with tempfile.TemporaryDirectory() as tmp:
        zipfile.ZipFile(zip_path).extractall(tmp)
        hits = [p.parent for p in Path(tmp).rglob("*") if p.name.lower() == "person.csv"]
        if not hits:
            raise FileNotFoundError(f"No person.csv inside {zip_path.name}")
        shutil.rmtree(target, ignore_errors=True)
        shutil.copytree(hits[0], target)
    zip_path.unlink()
    print(f"{year}: saved to {target.relative_to(PROJECT_DIR)}")


def main(years):
    for year in years:
        download_year(year)
