"""Stage 4 (optional report): feature association per block -> processed/reports/.

python project/scripts/04_multicollinearity.py 2016
"""

import _path  # noqa: F401

from fars import cli, multicollinearity

if __name__ == "__main__":
    args = cli.parse(cli.parser(__doc__.splitlines()[0]))
    multicollinearity.main(args.years, args.population)
