"""Run the per-year pipeline: preprocess, then the decision trees, for each year.

--mc adds the multicollinearity report between the two. The report only flags related
features; it changes nothing (columns are dropped only via DROP_COLS in
fars/config.py). Stages 1-2 (download, load) are run once, separately.

    python project/scripts/run.py full                          every year
    python project/scripts/run.py 2016 2023                     individual years
    python project/scripts/run.py full --mc                     + the multicollinearity report
    python project/scripts/run.py 2019 --block AB_crash         trees for one block only
"""

import _path  # noqa: F401

from fars import cli, decision_tree, multicollinearity, preprocess

if __name__ == "__main__":
    p = cli.parser("Run the per-year pipeline: preprocess, then decision trees", block=True)
    p.add_argument(
        "--mc",
        action="store_true",
        help="also write the multicollinearity report (report only; changes nothing)",
    )
    args = cli.parse(p)
    blocks = [args.block] if args.block else None
    for year in args.years:
        preprocess.run(year, args.population)
        if args.mc:
            multicollinearity.run(year, args.population)
        decision_tree.run(year, args.population, blocks)
