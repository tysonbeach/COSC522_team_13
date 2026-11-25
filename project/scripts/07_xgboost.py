"""Stage 7: XGBoost per year and block -> processed/results/xgboost/.

Needs the decision-tree split manifest for the same year and population (stage 5).

python project/scripts/07_xgboost.py 2016 --population restricted
python project/scripts/07_xgboost.py full --population full
python project/scripts/07_xgboost.py 2019 --block A_precrash
"""

import _path  # noqa: F401

from fars import cli, xgboost_model

if __name__ == "__main__":
    args = cli.parse(cli.parser(__doc__.splitlines()[0], block=True))
    xgboost_model.main(args.years, args.population, [args.block] if args.block else None)
