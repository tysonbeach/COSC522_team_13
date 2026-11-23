"""Stage 5: decision trees per year and block -> processed/results/decision_tree/.

python project/scripts/05_decision_tree.py full                 every year, all blocks
python project/scripts/05_decision_tree.py 2019 --block A_precrash
"""

import _path  # noqa: F401

from fars import cli, decision_tree

if __name__ == "__main__":
    args = cli.parse(cli.parser(__doc__.splitlines()[0], block=True))
    decision_tree.main(args.years, args.population, [args.block] if args.block else None)
