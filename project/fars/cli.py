"""Shared command-line arguments for the scripts in project/scripts/.

Years are required and given one of two ways:
    full                 every year, 2016-2023
    2016 2019 2023       individual years, separated by spaces
"""

import argparse

from .config import BLOCKS, DEFAULT_POPULATION, POPULATIONS, YEARS

ALL_YEARS = "full"


def parse_years(items):
    """["full"] -> every year; ["2016", "2019"] -> [2016, 2019]."""
    if items == [ALL_YEARS]:
        return list(YEARS)
    if ALL_YEARS in items:
        raise ValueError(f"give either '{ALL_YEARS}' or individual years, not both")
    bad = [i for i in items if not (i.isdigit() and int(i) in YEARS)]
    if bad:
        raise ValueError(
            f"invalid year(s) {bad}: give '{ALL_YEARS}' or years {YEARS[0]}-{YEARS[-1]} "
            "separated by spaces, e.g. 2016 2019"
        )
    return [int(i) for i in items]


def parser(description, years=True, population=True, block=False):
    """An ArgumentParser with the usual arguments."""
    p = argparse.ArgumentParser(description=description)
    if years:
        p.add_argument(
            "years",
            nargs="+",
            metavar="YEARS",
            help=f"'{ALL_YEARS}' for every year {YEARS[0]}-{YEARS[-1]}, "
            "or individual years separated by spaces, e.g. 2016 2019",
        )
    if population:
        p.add_argument("--population", choices=POPULATIONS, default=DEFAULT_POPULATION)
    if block:
        p.add_argument("--block", choices=BLOCKS, help="run only this feature block (default: all)")
    return p


def parse(p):
    """Parse args and turn the years argument into a list of ints."""
    args = p.parse_args()
    if hasattr(args, "years"):
        try:
            args.years = parse_years(args.years)
        except ValueError as e:
            p.error(str(e))
    return args
