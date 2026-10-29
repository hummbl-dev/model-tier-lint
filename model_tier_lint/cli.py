"""model-tier-lint CLI.

    python -m model_tier_lint lint catalog.json
"""

import argparse
import sys

from .lint import lint_file


def cmd_lint(args) -> int:
    ok, errors = lint_file(args.catalog)
    for e in errors:
        print(e)
    print(f"{'VALID' if ok else 'INVALID'}: {args.catalog}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="model-tier-lint", description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    l = sub.add_parser("lint", help="lint a tier catalog")
    l.add_argument("catalog")
    l.set_defaults(fn=cmd_lint)
    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
