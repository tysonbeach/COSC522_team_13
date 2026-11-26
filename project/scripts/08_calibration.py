"""Stage 8: calibration of the tuned XGBoost -> processed/results/xgboost_calibration/.

Needs the XGBoost results (stage 7: best_params, holdout metrics, split manifest) and the
decision-tree split manifest for the same year and population.

python project/scripts/08_calibration.py 2016 --population restricted
python project/scripts/08_calibration.py full --population full
python project/scripts/08_calibration.py 2019 --block ABC_post
"""

import _path  # noqa: F401

from fars import calibration, cli

if __name__ == "__main__":
    args = cli.parse(cli.parser(__doc__.splitlines()[0], block=True))
    calibration.main(args.years, args.population, [args.block] if args.block else None)
