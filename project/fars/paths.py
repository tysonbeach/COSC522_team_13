"""Where every stage reads and writes its files.

processed/
  joined/fars_<YEAR>_person.parquet                         load.py
  datasets/<POPULATION>/<YEAR>/                              preprocess.py
      dataset_<YEAR>.csv, features_<YEAR>.json,
      recode_audit_<YEAR>.csv, medium_truck_counts_<YEAR>.csv
  reports/multicollinearity/<POPULATION>/<YEAR>/<BLOCK>/     multicollinearity.py
  results/<MODEL>/<POPULATION>/<YEAR>/                       decision_tree.py, ...
      holdout_split_<YEAR>_seed522.csv
      <BLOCK>/<name>_<BLOCK>_<YEAR>.csv, summary_*.md, figures/*.png

Block and year stay in result file names, so a file is still identifiable when copied
out of its folder.
"""

from .config import DATA_DIR, DATASETS_DIR, JOINED_DIR, REPORTS_DIR, RESULTS_DIR


def raw_dir(year):
    return DATA_DIR / f"FARS{year}NationalCSV"


def joined_path(year):
    return JOINED_DIR / f"fars_{year}_person.parquet"


def dataset_dir(population, year):
    return DATASETS_DIR / population / str(year)


def dataset_path(population, year):
    return dataset_dir(population, year) / f"dataset_{year}.csv"


def features_path(population, year):
    return dataset_dir(population, year) / f"features_{year}.json"


def report_dir(report, population, year, block):
    return REPORTS_DIR / report / population / str(year) / block


def results_dir(model, population, year):
    return RESULTS_DIR / model / population / str(year)


def block_dir(model, population, year, block):
    return results_dir(model, population, year) / block


def require(path, made_by):
    """Fail with a clear message if an input from an earlier stage is missing."""
    if not path.exists():
        raise FileNotFoundError(f"Missing {path}. Run {made_by} first.")
    return path
