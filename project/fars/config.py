"""Project-wide settings: paths, years, columns, feature blocks and modeling constants.

Everything the pipeline stages share is defined here once. Stage-specific settings
(e.g. the decision-tree grid) live in the stage's own module.
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# Paths (anchored to this file, so scripts work from any directory)
# ---------------------------------------------------------------------------
PROJECT_DIR = Path(__file__).resolve().parent.parent  # project/
DATA_DIR = PROJECT_DIR / "data"  # raw FARS CSVs (download.py)
PROCESSED_DIR = PROJECT_DIR / "processed"
JOINED_DIR = PROCESSED_DIR / "joined"  # one person-level table per year (load.py)
DATASETS_DIR = PROCESSED_DIR / "datasets"  # modeling datasets (preprocess.py)
REPORTS_DIR = PROCESSED_DIR / "reports"  # descriptive reports (multicollinearity.py)
RESULTS_DIR = PROCESSED_DIR / "results"  # model results (decision_tree.py, ...)

# ---------------------------------------------------------------------------
# Years, populations, reproducibility
# ---------------------------------------------------------------------------
YEARS = range(2016, 2024)  # 2016-2023
POPULATIONS = ("full", "restricted")  # restricted: no motorcycles; at least two modeled occupants per crash
DEFAULT_POPULATION = "full"
SEED = 522
N_JOBS = 2

# ---------------------------------------------------------------------------
# Columns
# ---------------------------------------------------------------------------
LABEL = "FATAL"  # 1 = died within 30 days (INJ_SEV 4), 0 = survived (INJ_SEV 0-3)
ID_COLS = ["ST_CASE", "VEH_NO", "PER_NO", "YEAR", "STATE", "INJ_SEV"]
CRASH_KEY = ["YEAR", "STATE", "ST_CASE"]  # one crash
PERSON_KEY = CRASH_KEY + ["VEH_NO", "PER_NO"]  # one occupant

# fmt: off
# Block A, pre-crash (26): fixed before the crash happens.
PRECRASH_COLS = [
    "AGE", "SEX", "PER_TYP", "SEAT_POS", "REST_USE",                   # person
    "BODY_TYP", "MOD_YEAR", "NUMOCCS", "TOW_VEH", "L_STATUS",          # vehicle, driver
    "VSPD_LIM", "VALIGN", "VPROFILE", "VSURCOND", "VTRAFWAY",          # road
    "VNUM_LAN", "VTRAFCON", "VTCONT_F",
    "HOUR", "DAY_WEEK", "MONTH",                                       # time
    "RUR_URB", "FUNC_SYS", "LGT_COND", "WEATHER", "RELJCT2",           # setting
]
# Block B, crash configuration (16 before drops): how the crash happened.
CRASH_COLS = [
    "IMPACT1", "P_CRASH1", "P_CRASH2", "PCRASH4", "PCRASH5",           # vehicle's crash
    "SPEEDREL", "DR_DRINK",                                            # driver
    "HARM_EV", "MAN_COLL", "REL_ROAD",                                 # crash
    "VE_FORMS", "PEDS", "PERNOTMVIT", "PERSONS", "PERMVIT", "DRUNK_DR",  # crash counts
]
# Block C, consequence (6): what the crash did to the vehicle and occupant.
POST_COLS = ["AIR_BAG", "EJECTION", "EXTRICAT", "ROLLOVER", "DEFORMED", "FIRE_EXP"]

NUMERIC_COLS = [
    "AGE", "MOD_YEAR", "NUMOCCS", "VSPD_LIM",
    "VE_FORMS", "PEDS", "PERNOTMVIT", "PERSONS", "PERMVIT",
]
# fmt: on
ALL_FEATURE_COLS = PRECRASH_COLS + CRASH_COLS + POST_COLS

# Feature columns removed from every block (decided after the multicollinearity report).
#   PERSONS: near-duplicate of PERMVIT (same in 99.5% of rows); PERSONS also counts
#            occupants of parked vehicles, PERMVIT only motorists in transport.
#   PEDS:    near-duplicate of PERNOTMVIT (same in 99.5% of rows); PERNOTMVIT also
#            counts occupants of parked vehicles as non-motorists.
#   Each pair split its importance between two bars; the MVIT versions are kept.
#   NUMOCCS: removed to reduce the occupant-count artifact in fatal-crash data.
#   PERNOTMVIT: excluded by the team decision on crash-count predictors.
DROP_COLS = ["PERSONS", "PEDS", "NUMOCCS", "PERNOTMVIT"]


def _without_drops(cols):
    return [c for c in cols if c not in DROP_COLS]


# The nested feature blocks, one model run each (report: Run 1 / 2 / 3). Every block
# models exactly the same occupants; only the features differ.
BLOCKS = {
    "A_precrash": _without_drops(PRECRASH_COLS),
    "AB_crash": _without_drops(PRECRASH_COLS + CRASH_COLS),
    "ABC_post": _without_drops(ALL_FEATURE_COLS),
}

# Rows with these codes in numeric columns are dropped from the cohort (unknowns).
UNKNOWN_CODES = {
    "AGE": [998, 999],
    "MOD_YEAR": [9998, 9999],
    "VSPD_LIM": [0, 98, 99],  # legacy rule: 0 is a substantive category, not unknown
}

# Medium-truck body types (descriptive count only; NHTSA manual Appendix C). Same
# meaning in every year 2016-2023 and untouched by the recodes.
MEDIUM_TRUCK_BODY_TYPES = {60, 61, 62, 64, 67, 71}

# NCSA motorcycle group (manual p. 139, Appendix C-29): includes mopeds,
# scooters and autocycles; excludes ATVs (90) and snowmobiles (91).
MOTORCYCLE_BODY_TYPES = frozenset(range(80, 90))

assert not set(DROP_COLS) - set(ALL_FEATURE_COLS), "DROP_COLS must be feature columns"
assert set(NUMERIC_COLS) <= set(ALL_FEATURE_COLS)
