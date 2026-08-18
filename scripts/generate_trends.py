from pathlib import Path
from collections import Counter
import argparse
import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "publication_trend.svg"

WIDTH, HEIGHT = 900, 320
MARGIN_L, MARGIN_R, MARGIN_T, MARGIN_B = 60, 20, 40, 50
PLOT_W = WIDTH - MARGIN_L - MARGIN_R
PLOT_H = HEIGHT - MARGIN_T - MARGIN_B


def render(papers):
    years = Counter(int(p["year"]) for p in papers)
    lo, hi = min(years), max(years)
    all_years = list(range(lo, hi + 1))
    counts = [years.get(y, 0) for y in all_years]
    max_count = max(counts) or 1
    n = len(all_years)
    slot = PLOT_W / n
    bar_w = max(18.0, slot * 0.55)

    def bar_x(i):
        return MARGIN_L + i * slot + (slot - bar_w) / 2

    def y_for(c):
        return MARGIN_T + PLOT_H * (1 - c / max_count)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" font-family="Arial, Helvetica, sans-serif">',
        f'<rect width="{WIDTH}" height="{HEIGHT}" rx="16" fill="#0d1117"/>',
        f'<text x="{WIDTH/2}" y="26" text-anchor="middle" font-size="16" font-weight="700" fill="#e6edf3">Aerial-Ground ReID papers per year (n = {len(papers)})</text>',
        # grid lines
    ]
    for g in range(0, max_count + 1):
        y = y_for(g)
        parts.append(f'<line x1="{MARGIN_L}" y1="{y:.1f}" x2="{WIDTH - MARGIN_R}" y2="{y:.1f}" stroke="#21262d" stroke-width="1"/>')
        parts.append(f'<text x="{MARGIN_L - 10}" y="{y + 4:.1f}" text-anchor="end" font-size="11" fill="#8b949e">{g}</text>')
    # bars
    for i, (year, c) in enumerate(zip(all_years, counts)):
        x = bar_x(i)
        y = y_for(c)
        h = PLOT_H * c / max_count
        if c:
            parts.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{h:.1f}" rx="4" fill="#3b82f6">'
                f'<title>{year}: {c} papers</title></rect>'
            )
            parts.append(f'<text x="{x + bar_w/2:.1f}" y="{y - 6:.1f}" text-anchor="middle" font-size="12" font-weight="700" fill="#79c0ff">{c}</text>')
        parts.append(f'<text x="{x + bar_w/2:.1f}" y="{MARGIN_T + PLOT_H + 20:.1f}" text-anchor="middle" font-size="12" fill="#8b949e">{year}</text>')
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    with open(ROOT / "data" / "papers.yaml", "r", encoding="utf-8") as f:
        papers = yaml.safe_load(f)["papers"]
    content = render(papers)
    if args.check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != content:
            raise SystemExit(f"{OUT.relative_to(ROOT)} is stale — run `python scripts/generate_trends.py`")
        print("Publication trend chart is up to date")
    else:
        OUT.write_text(content, encoding="utf-8")
        print("wrote", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
