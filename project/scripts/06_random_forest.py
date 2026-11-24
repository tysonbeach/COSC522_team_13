"""Stage 6: random forests per year and block -> processed/results/random_forest/.

Needs the decision-tree split manifest for the same year and population (stage 5).

python project/scripts/06_random_forest.py 2016 --population restricted
python project/scripts/06_random_forest.py full --population full
python project/scripts/06_random_forest.py 2019 --block A_precrash
"""

import _path  # noqa: F401

from fars import cli, random_forest

if __name__ == "__main__":
    args = cli.parse(cli.parser(__doc__.splitlines()[0], block=True))
    random_forest.main(args.years, args.population, [args.block] if args.block else None)
