"""Stage 1: download the FARS national CSVs into project/data/ (skips years present).

python project/scripts/01_download.py full         every year, 2016-2023
python project/scripts/01_download.py 2019 2021
"""

import _path  # noqa: F401

from fars import cli, download

if __name__ == "__main__":
    args = cli.parse(cli.parser(__doc__.splitlines()[0], population=False))
    download.main(args.years)
