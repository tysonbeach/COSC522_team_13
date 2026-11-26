"""Stage 9: SHAP values of the tuned XGBoost -> processed/results/xgboost_shap/.

Needs the XGBoost results (stage 7: best_params, holdout metrics, split manifest) and the
decision-tree split manifest for the same year and population.

python project/scripts/09_shap.py 2016 --population restricted
python project/scripts/09_shap.py full --population full
python project/scripts/09_shap.py 2019 --block ABC_post
"""

import _path  # noqa: F401

from fars import cli, shap_values

if __name__ == "__main__":
    args = cli.parse(cli.parser(__doc__.splitlines()[0], block=True))
    shap_values.main(args.years, args.population, [args.block] if args.block else None)
