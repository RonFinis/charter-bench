"""Build index.html (a full standalone page for GitHub Pages) from charter-bench.html.

charter-bench.html is the single source of truth. It is written as a page fragment
(no <html>/<head>/<body>) because that is the format the Claude artifact uses.
This script wraps it in a proper document so it works on any web host.

Usage:  python build.py
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "charter-bench.html"
OUT = HERE / "index.html"

FAVICON = (
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 28 28'%3E"
    "%3Crect x='1' y='1' width='26' height='26' rx='6' fill='%23B3202A'/%3E"
    "%3Cpath d='M7 20h14M9 20V12M14 20V12M19 20V12M6 12h16L14 6.5z' stroke='%23fff' "
    "stroke-width='1.8' fill='none' stroke-linejoin='round'/%3E%3C/svg%3E"
)

# Reset rules the artifact host normally supplies.
BASE_CSS = """<style>
html{-webkit-text-size-adjust:100%}
:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
body{margin:0}
img{max-width:100%}
</style>"""


def main() -> None:
    src = SRC.read_text(encoding="utf-8")
    cut = src.index("</style>") + len("</style>")
    head, body = src[:cut], src[cut:]
    head = head.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
    page = (
        "<!doctype html>\n<html lang=\"en\">\n<head>\n"
        f"{head}\n"
        '<meta name="description" content="Study site for the Grade 12 Canadian &amp; International Law '
        'Unit 2 test: the Charter, s. 35 Indigenous rights and human rights.">\n'
        f'<link rel="icon" href="{FAVICON}">\n'
        f"{BASE_CSS}\n</head>\n<body>\n{body.strip()}\n</body>\n</html>\n"
    )
    OUT.write_text(page, encoding="utf-8", newline="\n")
    print(f"Wrote {OUT.name} ({len(page):,} bytes)")


if __name__ == "__main__":
    main()
