"""Stage 2: join Person -> Vehicle -> Accident into processed/joined/ (run once).

python project/scripts/02_load.py full             every year, 2016-2023
python project/scripts/02_load.py 2023
"""

import _path  # noqa: F401

from fars import cli, load

if __name__ == "__main__":
    args = cli.parse(cli.parser(__doc__.splitlines()[0], population=False))
    load.main(args.years)
