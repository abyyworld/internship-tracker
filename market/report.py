"""Write docs/market.html from market/results.json.

The page is static: the results are embedded, and the charts are drawn in the
browser from them, so it works from GitHub Pages and from a local file alike.

Run:   python -m market.report   (after python -m market.analysis)
"""

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "market" / "results.json"
TEMPLATE = ROOT / "market" / "report_template.html"
PAGE = ROOT / "docs" / "market.html"
MARK = "/*RESULTS*/null"


def render(results, template=TEMPLATE):
    page = Path(template).read_text()
    if MARK not in page:
        raise ValueError(f"{template} has no {MARK} placeholder")
    # "</" cannot appear inside the script block; JSON allows "<\/".
    data = json.dumps(results, separators=(",", ":")).replace("</", "<\\/")
    return page.replace(MARK, data)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--results", default=str(RESULTS))
    parser.add_argument("--out", default=str(PAGE))
    args = parser.parse_args(argv)
    results = json.loads(Path(args.results).read_text())
    Path(args.out).write_text(render(results))
    print(f"report -> {args.out}")


if __name__ == "__main__":
    main()
