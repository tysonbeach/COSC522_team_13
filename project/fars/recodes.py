"""Year-to-year code harmonization, so every year 2016-2023 uses the same codes.

Each rule maps codes a year used onto the code later years use for the same thing. A
rule only fires for its own years (last = None means "and every later year"). Sources:
fars_variable_lists.xlsx, plus a full check of all 26 block-A columns against the FARS
Analytical User's Manual 1975-2024 (page numbers are the manual's printed numbers).

Where FARS added a new code, the cases it covers were filed under an older code in
earlier years, so the new code is merged back into that older code.

JUDGMENT CALLS. Two rules map a new code whose earlier home cannot be pinned down from
the manual or the data (their reason, which also goes into recode_audit_<YEAR>.csv,
starts with "JUDGMENT CALL"):
  - VTRAFWAY 7 -> 9: "two-way divided, unknown median type" (2022+) was previously
    coded 2, 3, or 9 depending on the report; 9 (unknown) is the closest single code.
    About 450-500 occupants per year.
  - REST_USE 6 -> 97: "racing-style harness" (2019+) was most likely coded 97 (Other)
    before; it may instead have been 8 (restraint used, type unknown). 2-11 per year.
Both affect few enough people that either choice barely moves the results.

DRUNK_DR was dropped from the accident file in 2021; it is rebuilt from DR_DRINK.
"""

from typing import NamedTuple

import pandas as pd


class Recode(NamedTuple):
    column: str
    first: int
    last: int | None  # None = every later year
    mapping: dict
    reason: str

    def applies_to(self, year):
        return self.first <= year and (self.last is None or year <= self.last)


# fmt: off
RECODES = [
    # --- from fars_variable_lists.xlsx ---
    Recode("REST_USE", 2016, 2016, {0: 20, 7: 20},
           "Not Applicable (0) and None Used (7) became None Used/Not Applicable (20) in 2017"),
    Recode("REST_USE", 2016, 2018, {5: 20, 16: 20, 17: 20, 19: 20, 29: 20},
           "helmet codes moved to HELM_USE in 2019; riders are coded 20 from 2019 (manual p. 304)"),
    Recode("BODY_TYP", 2016, 2016, {30: 34, 31: 34},
           "Compact (30) and Standard (31) Pickup became Light Pickup (34) in 2017"),
    Recode("BODY_TYP", 2016, 2017, {32: 34},
           "Pickup With Slide-in Camper (32) retired after 2017 (manual p. 137)"),
    Recode("AIR_BAG", 2016, 2016, {0: 20},
           "Not Applicable (0) is coded Not Deployed (20) from 2017"),
    Recode("ROLLOVER", 2016, 2021, {1: 3, 2: 3, 9: 3},
           "tripped/untripped/unknown-type rollovers collapsed into Rollover (3) in 2022"),
    Recode("ROLLOVER", 2022, None, {8: 0},
           "Not Applicable (8) split off from No Rollover (0) in 2022; merged back"),
    Recode("DEFORMED", 2022, None, {7: 8},
           "Damage Reported, Extent Unknown (7) split off from Not Reported (8) in 2022; "
           "merged back"),
    # --- from the full manual check of the block-A columns ---
    Recode("BODY_TYP", 2017, None, {84: 88},
           "Motor Scooter (84) split off from Other Motored Cycle (88) in 2017 (manual p. 139)"),
    Recode("BODY_TYP", 2017, None, {85: 82, 86: 82, 87: 82},
           "autocycle/three-wheel codes 85-87 split off from Three-Wheel Motorcycle (82) "
           "in 2017 (manual p. 139)"),
    Recode("BODY_TYP", 2017, None, {96: 97},
           "off-highway utility vehicles (96) split off from Other Vehicle Type (97) in "
           "2017 (manual p. 140)"),
    Recode("SEAT_POS", 2019, None, {56: 55},
           "Appended to a Motor Vehicle for Motion (56) split off from Riding on Vehicle "
           "Exterior (55) in 2019 (manual p. 302)"),
    Recode("TOW_VEH", 2022, None, {7: 1},
           "Trailing Unit Other than a Trailer (7) split off in 2022; before 2022 any "
           "trailing unit was 1 (manual pp. 144-145)"),
    Recode("VTCONT_F", 2016, None, {2: 1, 4: 1},
           "Not Functioning (1), Functioning Improperly (2) and the 2019+ combined code "
           "(4) merged into 1 in all years, since 4 cannot be split back (manual p. 232)"),
    Recode("VTRAFWAY", 2022, None, {7: 9},
           "JUDGMENT CALL: Divided, Unknown Median Type (7, 2022+) was coded 2, 3 or 9 "
           "before; mapped to 9 (unknown) as the closest single code (manual p. 223)"),
    Recode("REST_USE", 2019, None, {6: 97},
           "JUDGMENT CALL: Racing-Style Harness (6, 2019+) most likely coded Other (97) "
           "before; could have been 8 (type unknown) (manual p. 304)"),
]
# fmt: on
AUDIT_COLUMNS = ["column", "years", "mapping", "rows_changed", "reason"]


def rebuild_drunk_dr(people):
    """DRUNK_DR = number of drinking drivers in the crash, i.e. vehicles with
    DR_DRINK == 1 per ST_CASE. Matches the published DRUNK_DR exactly for 2016-2020."""
    vehicles = people.dropna(subset=["DR_DRINK"]).drop_duplicates(["ST_CASE", "VEH_NO"])
    per_crash = vehicles["DR_DRINK"].eq(1).groupby(vehicles["ST_CASE"]).sum()
    return people["ST_CASE"].map(per_crash).fillna(0).astype(int)


def apply_recodes(df, year):
    """Apply this year's rules and the DRUNK_DR rebuild to df in place.
    Returns an audit table with one row per rule that fired."""
    audit = []
    for rule in RECODES:
        if not rule.applies_to(year):
            continue
        hit = df[rule.column].isin(list(rule.mapping))
        df.loc[hit, rule.column] = df.loc[hit, rule.column].map(rule.mapping)
        audit.append(
            {
                "column": rule.column,
                "years": f"{rule.first}-{rule.last or 'later'}",
                "mapping": str(rule.mapping),
                "rows_changed": int(hit.sum()),
                "reason": rule.reason,
            }
        )

    rebuilt = rebuild_drunk_dr(df)
    if "DRUNK_DR" in df:
        mismatches = int((rebuilt != df["DRUNK_DR"]).sum())
        print(f"DRUNK_DR present; rebuild check: {mismatches:,} mismatching rows")
    else:
        df["DRUNK_DR"] = rebuilt
        audit.append(
            {
                "column": "DRUNK_DR",
                "years": "2021-later",
                "mapping": "rebuilt from DR_DRINK",
                "rows_changed": len(df),
                "reason": "DRUNK_DR removed from the accident file in 2021",
            }
        )
    return pd.DataFrame(audit, columns=AUDIT_COLUMNS)
