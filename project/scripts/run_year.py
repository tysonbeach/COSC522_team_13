"""Run the full per-year pipeline: preprocessing.py, then decision_tree.py.

Outputs go to processed/decision_tree/<YEAR>/preprocessing/ and
.../<YEAR>/results/<TIER>/ (one folder per feature tier).
Requires the loaded table from init_load.py:
    processed/preprocessed/fars_<YEAR>_person.parquet

Run from anywhere, e.g. the repo root:
    python project/scripts/run_year.py 2019              one year
    python project/scripts/run_year.py 2017 2018 2019    several years, in order
"""

import argparse
import sys

sys.dont_write_bytecode = True  # keep __pycache__ out of project/scripts/

import decision_tree  # noqa: E402  (imported after the bytecode setting on purpose)
import preprocessing  # noqa: E402

VALID_YEARS = range(2016, 2024)


def parse_years():
    parser = argparse.ArgumentParser(
        description="Run preprocessing.py, then decision_tree.py, for FARS year(s)"
    )
    parser.add_argument(
        "years",
        nargs="+",
        type=int,
        choices=VALID_YEARS,
        metavar="YEAR",
        help="FARS year(s), 2016-2023",
    )
    return parser.parse_args().years


def run_year(year):
    print(f"\n{'=' * 30} {year}: preprocessing {'=' * 30}")
    preprocessing.main(year)
    print(f"\n{'=' * 30} {year}: decision tree {'=' * 30}")
    decision_tree.main(year)


def main():
    for year in parse_years():
        run_year(year)


if __name__ == "__main__":
    main()
