"""Stage 3: recodes + cohort -> processed/datasets/<POPULATION>/<YEAR>/.

python project/scripts/03_preprocess.py full             every year
python project/scripts/03_preprocess.py 2016 2017 2018  individual years
"""

import _path  # noqa: F401

from fars import cli, preprocess

if __name__ == "__main__":
    args = cli.parse(cli.parser(__doc__.splitlines()[0]))
    preprocess.main(args.years, args.population)
