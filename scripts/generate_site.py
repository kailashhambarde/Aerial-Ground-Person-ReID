from pathlib import Path
from html import escape
import argparse
import json
import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "index.html"
ROBOTS = ROOT / "robots.txt"
SITEMAP = ROOT / "sitemap.xml"

REPO = "kailashhambarde/Aerial-Ground-Person-ReID"
REPO_URL = f"https://github.com/{REPO}"
RAW = f"https://raw.githubusercontent.com/{REPO}/main"

GROUPS = [
    ("Image-based Person AG-ReID", {"image-ag-reid", "single-view-ag-reid", "text-ag-reid", "multimodal-ag-reid"}),
    ("Image-based Vehicle AG-ReID", {"image-vehicle-ag-reid"}),
    ("Video-based Person AG-ReID", {"video-ag-reid"}),
    ("Challenges & Workshops", {"challenge"}),
    ("More Related Exploration", {"related"}),
]

TAXONOMY = [
    ("View-invariant representation", ["VDT", "VIF-AGReID"]),
    ("View-aware representation", ["ViSA", "HiHR"]),
    ("Geometry & spatial alignment", ["GSAlign", "GeoReID", "3D-LENS"]),
    ("Semantic & vision-language alignment", ["SeCap", "ViSA", "HiHR"]),
    ("Temporal & video modeling", ["AG-VPReID-Net", "DFGS + uncertainty fusion", "EAGLE-ReID"]),
    ("Extreme-distance ReID", ["DetReIDX baselines"]),
    ("Multimodal / any-scenario ReID", ["UAD", "AG-VPReID.VIR"]),
    ("Single-view & domain-generalized", ["3D-LENS"]),
    ("Training-free / foundation models", ["DINO", "CLIP", "SigLIP"]),
]

CATEGORY_COLORS = {
    "Image.Person": "#3b82f6",
    "Video.Person": "#8b5cf6",
    "Image.Animal": "#22c55e",
    "Multimodal.Person": "#f59e0b",
    "Text.Person": "#ec4899",
}

CSS = """
:root {
  --bg: #ffffff; --fg: #1f2328; --muted: #59636e; --line: #d1d9e0;
  --card: #f6f8fa; --chip: #eef1f4; --link: #0969da; --hl: #fef3c7;
  --navbg: rgba(255,255,255,.86);
  --serif: Georgia, "Times New Roman", "Charter", serif;
  --sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0d1117; --fg: #e6edf3; --muted: #8b949e; --line: #30363d;
    --card: #161b22; --chip: #21262d; --link: #58a6ff; --hl: #3d2f00;
    --navbg: rgba(13,17,23,.86);
  }
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body { margin: 0; background: var(--bg); color: var(--fg);
  font-family: var(--sans); line-height: 1.6; }
.wrap { max-width: 1080px; margin: 0 auto; padding: 18px 20px 60px; }
a { color: var(--link); text-decoration: none; }
a:hover { text-decoration: underline; }

/* ---- sticky nav ---- */
.topnav { position: sticky; top: 10px; z-index: 50; display: flex; align-items: center;
  justify-content: space-between; gap: 12px; flex-wrap: wrap; background: var(--navbg);
  backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px);
  border: 1px solid var(--line); border-radius: 10px; padding: 8px 14px; margin-bottom: 22px; }
.brand { font-family: var(--serif); font-weight: 700; font-size: 15px; color: var(--fg); letter-spacing: .02em; }
.brand small { color: var(--muted); font-weight: 400; }
.nav-links { display: flex; flex-wrap: wrap; gap: 2px 14px; font-size: 14px; }
.nav-links a { color: var(--muted); padding: 3px 4px; border-radius: 6px; }
.nav-links a:hover { color: var(--link); text-decoration: none; }
.nav-links a.active { color: var(--link); font-weight: 600; background: var(--chip); }

/* ---- hero ---- */
header { text-align: center; padding: 10px 0 8px; }
.repo-line { display: inline-flex; align-items: center; gap: 8px; background: var(--chip);
  border: 1px solid var(--line); border-radius: 999px; padding: 6px 14px; font-size: 14px;
  color: var(--muted); text-decoration: none; }
.repo-line svg { flex: none; }
.repo-line b { color: var(--fg); font-weight: 600; }
.repo-line:hover { border-color: var(--link); text-decoration: none; }
h1 { font-family: var(--serif); font-size: 34px; font-weight: 700; margin: 16px 0 6px; letter-spacing: -.01em; }
.sub { color: var(--muted); margin: 0 0 16px; font-size: 16px; }
.actions { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin-bottom: 20px; }
.btn { display: inline-flex; align-items: center; gap: 6px; padding: 8px 16px; border-radius: 8px;
  border: 1px solid var(--line); background: var(--card); color: var(--fg); font-size: 14px;
  font-weight: 600; text-decoration: none; }
.btn:hover { border-color: var(--link); text-decoration: none; }
.btn-primary { background: #1f883d; border-color: #1f883d; color: #fff; }
.btn-primary:hover { background: #1a7f37; border-color: #1a7f37; }
.stats { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin-bottom: 20px; }
.chip { background: var(--chip); border: 1px solid var(--line); border-radius: 999px;
  padding: 6px 14px; font-size: 13px; }
.chip b { color: var(--link); }
#search { width: 100%; max-width: 620px; padding: 11px 16px; font-size: 15px;
  border-radius: 8px; border: 1px solid var(--line); background: var(--card); color: var(--fg); }
#search:focus { outline: 2px solid var(--link); outline-offset: -1px; }
#counter { color: var(--muted); font-size: 13px; margin: 8px 0 0; }

/* ---- sections ---- */
main section[id] { scroll-margin-top: 84px; }
h2 { font-family: var(--serif); font-size: 25px; font-weight: 700; border-bottom: 1px solid var(--line);
  padding-bottom: 8px; margin: 40px 0 6px; letter-spacing: -.01em; }
h2 .no { color: var(--muted); font-weight: 400; margin-right: 8px; font-size: 15px; }
h3 { font-family: var(--serif); font-size: 18px; margin: 26px 0 10px; }
.summary { color: var(--muted); font-size: 14px; margin: 4px 0 16px; }
.abstract { font-family: var(--serif); font-size: 16.5px; max-width: 760px; margin: 18px auto 8px;
  text-align: justify; border-left: 3px solid var(--link); padding-left: 18px; }
.keywords { color: var(--muted); font-size: 13.5px; margin: 14px auto 0; max-width: 760px; }
.keywords b { color: var(--fg); font-variant-caps: all-small-caps; letter-spacing: .06em; }
table { width: 100%; border-collapse: collapse; font-size: 14px; background: var(--card);
  border: 1px solid var(--line); border-radius: 8px; overflow: hidden; }
th, td { text-align: left; padding: 8px 12px; border-bottom: 1px solid var(--line); vertical-align: top; }
th { background: var(--chip); font-size: 12px; text-transform: uppercase; letter-spacing: .04em; color: var(--muted); }
tbody tr:nth-child(even) { background: rgba(127,127,127,.05); }
tbody tr:hover { background: var(--hl); }
tbody tr:last-child td { border-bottom: none; }
.venue { white-space: nowrap; font-weight: 700; }
.method { font-weight: 700; }
.tag { display: inline-block; padding: 1px 8px; border-radius: 999px; font-size: 11px;
  font-weight: 600; color: #fff; white-space: nowrap; }
.geom { color: var(--muted); font-size: 13px; }
.trend-svg { width: 100%; height: auto; max-width: 860px; border-radius: 12px;
  border: 1px solid var(--line); display: block; margin: 6px auto 0; }
.notes { background: var(--card); border: 1px solid var(--line); border-radius: 8px; padding: 12px 16px; }
.notes li { margin: 4px 0; }

/* ---- footer ---- */
footer { text-align: center; color: var(--muted); font-size: 13px; margin-top: 56px;
  border-top: 1px solid var(--line); padding-top: 22px; }
footer code { background: var(--chip); padding: 1px 5px; border-radius: 4px; }
.cite { max-width: 640px; margin: 14px auto 4px; text-align: left; background: var(--card);
  border: 1px solid var(--line); border-radius: 8px; padding: 12px 16px; overflow-x: auto;
  font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 12.5px; line-height: 1.5; }
.footer-links { display: flex; flex-wrap: wrap; gap: 4px 14px; justify-content: center; margin-top: 10px; }
@media (max-width: 720px) { .venue, th, td { white-space: normal; } }
"""

GITHUB_SVG = (
    '<svg viewBox="0 0 16 16" width="16" height="16" fill="currentColor" aria-hidden="true">'
    '<path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8Z"/></svg>'
)

STAR_SVG = (
    '<svg viewBox="0 0 16 16" width="16" height="16" fill="currentColor" aria-hidden="true">'
    '<path d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Z"/></svg>'
)


def esc(s):
    return escape(str(s or "—"))


def fmt_num(v):
    return f"{int(v):,}" if v else "—"


def fmt_list(v):
    return ", ".join(v) if v else "—"


def resources(p):
    parts = [f'<a href="{esc(p["paper"])}">Paper</a>']
    if p.get("code"):
        parts.append(f'<a href="{esc(p["code"])}">Code</a>')
    if p.get("dataset_url"):
        parts.append(f'<a href="{esc(p["dataset_url"])}">Dataset</a>')
    return " · ".join(parts)


def method_cell(method):
    return f'<span class="method">{esc(method)}</span>' if method and method != "—" else "—"


def papers_html(papers):
    by_task = {task: g for g, tasks in GROUPS for task in tasks}
    buckets = {g: [] for g, _ in GROUPS}
    for p in papers:
        task = p.get("task")
        if task not in by_task:
            raise SystemExit(f"Unknown task '{task}' for paper {p.get('id')}")
        buckets[by_task[task]].append(p)
    out = []
    for g, _ in GROUPS:
        group = sorted(buckets[g], key=lambda x: (-int(x["year"]), x["method"].lower()))
        if not group:
            continue
        rows = "".join(
            f"<tr><td class=\"venue\">{esc(p['venue'])} {p['year']}</td>"
            f"<td>{method_cell(p.get('method'))}</td>"
            f"<td>{esc(p['title'])}</td>"
            f"<td>{resources(p)}</td></tr>"
            for p in group
        )
        out.append(
            f'<section data-group><h3>{esc(g)}</h3>'
            f'<table><thead><tr><th>Conference / Journal</th><th>Method</th><th>Title</th><th>Resources</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></section>'
        )
    return "\n".join(out)


def taxonomy_html():
    rows = "".join(
        f"<tr><td>{esc(family)}</td><td>{', '.join(esc(m) for m in methods)}</td></tr>"
        for family, methods in TAXONOMY
    )
    return (
        '<table id="taxonomy-table"><thead><tr><th>Research family</th><th>Representative methods</th></tr></thead>'
        f"<tbody>{rows}</tbody></table>"
    )


def datasets_html(datasets):
    rows = []
    for d in sorted(datasets, key=lambda x: (int(x["year"]), x["name"].lower())):
        scale = []
        if d.get("images"):
            scale.append(f"{int(d['images']):,} images")
        if d.get("tracklets"):
            scale.append(f"{int(d['tracklets']):,} tracklets")
        if d.get("frames"):
            scale.append(f"{int(d['frames']):,} frames")
        if d.get("boxes"):
            scale.append(f"{int(d['boxes']):,} boxes")
        geom = []
        if d.get("altitude_m"):
            geom.append(f"alt. {d['altitude_m']} m")
        if d.get("distance_m"):
            geom.append(f"dist. {d['distance_m']} m")
        cat = d.get("category") or "—"
        color = CATEGORY_COLORS.get(cat, "#6e7781")
        download = f'<a href="{esc(d["download"])}">download</a>' if d.get("download") else "—"
        rows.append(
            f"<tr><td><a href=\"{esc(d['source'])}\"><b>{esc(d['name'])}</b></a></td>"
            f"<td>{d['year']}</td>"
            f"<td><span class=\"tag\" style=\"background:{color}\">{esc(cat)}</span></td>"
            f"<td>{fmt_num(d.get('identities'))}</td>"
            f"<td>{'; '.join(scale) or '—'}</td>"
            f"<td>{fmt_list(d.get('platforms'))}</td>"
            f"<td>{fmt_list(d.get('modalities'))}</td>"
            f"<td>{'✓' if d.get('video') else '—'}</td>"
            f"<td class=\"geom\">{'; '.join(geom) or '—'}</td>"
            f"<td>{download}</td></tr>"
        )
    return (
        '<table id="datasets-table"><thead><tr>'
        "<th>Dataset</th><th>Year</th><th>Category</th><th>IDs</th><th>Scale</th>"
        "<th>Platforms</th><th>Modalities</th><th>Video</th><th>Geometry</th><th>Download</th>"
        f"</tr></thead><tbody>{''.join(rows)}</tbody></table>"
    )


def notes_html(datasets):
    items = [f"<li><b>{esc(d['name'])}</b>: {esc(d['notes'])}</li>" for d in sorted(datasets, key=lambda x: x["name"].lower()) if d.get("notes")]
    return f'<ul class="notes">{"".join(items)}</ul>'


def trend_svg_html():
    """Inline the generated trend chart so index.html stays fully self-contained."""
    svg = (ROOT / "assets" / "publication_trend.svg").read_text(encoding="utf-8")
    return svg.replace(
        "<svg ",
        '<svg class="trend-svg" role="img" aria-label="Bar chart of aerial-ground person ReID papers per year" ',
        1,
    )


def json_ld(papers, datasets):
    graph = [
        {
            "@type": "WebSite",
            "name": "Aerial-Ground Person Re-Identification",
            "alternateName": "AGPReID Resource",
            "url": REPO_URL,
            "description": "A protocol-aware, machine-readable resource of papers, datasets, benchmarks and evaluation protocols for aerial-ground person re-identification (AGPReID).",
            "inLanguage": "en",
            "publisher": {"@type": "Person", "name": "Kailash A. Hambarde"},
        }
    ]
    for p in sorted(papers, key=lambda x: (-int(x["year"]), x["method"].lower())):
        graph.append({
            "@type": "ScholarlyArticle",
            "name": p["title"],
            "headline": p["title"],
            "url": p["paper"],
            "datePublished": str(p["year"]),
            "publisher": {"@type": "Organization", "name": p["venue"]},
            "keywords": ", ".join(p.get("categories", []) or []),
            "isPartOf": {"@type": "CreativeWork", "name": "Aerial-Ground Person Re-Identification: Papers, Datasets, Benchmarks and Research Resources", "url": REPO_URL},
        })
    for d in sorted(datasets, key=lambda x: (int(x["year"]), x["name"].lower())):
        entry = {
            "@type": "Dataset",
            "name": d["name"],
            "url": d["source"],
            "datePublished": str(d["year"]),
            "keywords": ", ".join([d.get("category") or "AG-ReID", ", ".join(d.get("platforms", []) or []), ", ".join(d.get("modalities", []) or [])]),
            "isAccessibleForFree": True,
            "isPartOf": {"@type": "CreativeWork", "name": "Aerial-Ground Person Re-Identification", "url": REPO_URL},
        }
        if d.get("identities"):
            entry["variableMeasured"] = f"{d['identities']} identities"
        if d.get("download"):
            entry["distribution"] = {"@type": "DataDownload", "name": f"{d['name']} download", "contentUrl": d["download"]}
        graph.append(entry)
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)


def head(papers, datasets):
    n = len(papers)
    dn = len(datasets)
    title = "Aerial-Ground Person Re-Identification — Papers, Datasets & Benchmarks"
    desc = (
        f"A curated, protocol-aware resource for Aerial-Ground Person Re-Identification (AGPReID): "
        f"{n} papers with links to code and datasets, {dn} datasets with download links, evaluation protocols, "
        "taxonomy, leaderboards and open problems. Machine-readable YAML/CSV data."
    )
    keywords = (
        "aerial-ground person re-identification, AG-ReID, AGPReID, UAV person re-identification, "
        "cross-view person re-identification, aerial-ground datasets, video person re-identification, "
        "multimodal re-identification, person retrieval benchmark, computer vision, deep learning"
    )
    og_image = f"{RAW}/assets/banner.svg"
    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="keywords" content="{esc(keywords)}">
<meta name="author" content="Kailash A. Hambarde">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{REPO_URL}/blob/main/index.html">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Aerial-Ground Person Re-Identification">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{REPO_URL}">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{og_image}">
<script type="application/ld+json">
{json_ld(papers, datasets)}
</script>"""


def nav():
    return f"""<nav class="topnav" aria-label="Section navigation">
<a class="brand" href="#top">AGPReID <small>· research index</small></a>
<div class="nav-links">
<a href="#about">About</a>
<a href="#papers">Papers</a>
<a href="#taxonomy">Taxonomy</a>
<a href="#datasets">Datasets</a>
<a href="#trends">Trends</a>
<a href="{REPO_URL}" target="_blank" rel="noopener">GitHub ↗</a>
</div>
</nav>"""


def hero(papers, datasets):
    n = len(papers)
    with_code = sum(1 for p in papers if p.get("code"))
    peer = sum(1 for p in papers if p.get("status") == "peer-reviewed")
    dn = len(datasets)
    total_ids = sum(int(d.get("identities") or 0) for d in datasets)
    video = sum(1 for d in datasets if d.get("video"))
    owner, repo = REPO.split("/", 1)
    return f"""
<header id="top">
<a class="repo-line" href="{REPO_URL}">{GITHUB_SVG}<span>github.com/<b>{esc(owner)}</b>/<b>{esc(repo)}</b></span></a>
<h1>Aerial-Ground Person Re-Identification</h1>
<p class="sub">Single-page index — papers, datasets, benchmarks and research resources for AGPReID.</p>
<div class="actions">
  <a class="btn btn-primary" href="{REPO_URL}/stargazers">{STAR_SVG} Star on GitHub</a>
  <a class="btn" href="{REPO_URL}/issues/new/choose">Open an issue</a>
  <a class="btn" href="README.md">View README</a>
</div>
<div class="stats">
<span class="chip"><b>{n}</b> papers</span>
<span class="chip"><b>{with_code}</b> with code</span>
<span class="chip"><b>{peer}</b> peer-reviewed</span>
<span class="chip"><b>{dn}</b> datasets</span>
<span class="chip"><b>{total_ids:,}</b> identities</span>
<span class="chip"><b>{video}</b> video benchmarks</span>
</div>
<input id="search" type="search" aria-label="Filter papers, datasets and taxonomy" placeholder="Filter everything — try “CVPR”, “video”, “prompt”, “Vehicle”" autocomplete="off">
<p id="counter"></p>
</header>"""


def render(papers, datasets):
    last_verified = max(str(p.get("verified_on", "")) for p in papers)
    cite = f"""@software{{hambarde2026agpreid,
  author = {{Hambarde, Kailash A.}},
  title  = {{Aerial-Ground Person Re-Identification: Papers, Datasets, Benchmarks and Research Resources}},
  year   = {{{last_verified[:4]}}},
  url    = {{{REPO_URL}}}
}}"""
    return f"""<!doctype html>
<html lang="en">
<head>
{head(papers, datasets)}
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
{nav()}
{hero(papers, datasets)}
<main>
<section id="about">
<h2><span class="no">§</span>About this resource</h2>
<p class="abstract">
Aerial-ground person re-identification (AGPReID) aims to match the same person across disjoint aerial and
ground camera views — a setting dominated by extreme viewpoint change, scale collapse, occlusion and
sensing-modality shifts. This index catalogues the methods, benchmarks and evaluation protocols of the field in
a single, machine-readable resource: {len(papers)} papers organised by the problem they solve, {len(datasets)} public
datasets with direct download links, and the protocol rules required for results to be compared fairly.
</p>
<p class="keywords"><b>Keywords</b>&nbsp; aerial-ground person re-identification · UAV surveillance · cross-view recognition · benchmarks · evaluation protocols · vision-language retrieval</p>
</section>

<section id="papers">
<h2><span class="no">1.</span>Papers &amp; methods</h2>
<p class="summary">Grouped by problem setting; each entry links to the paper, code and dataset.</p>
{papers_html(papers)}
</section>

<section id="taxonomy">
<h2><span class="no">2.</span>Method taxonomy</h2>
<p class="summary">Research families as organised in <a href="docs/taxonomy.md">docs/taxonomy.md</a> — methods are grouped by the problem they solve, not by venue.</p>
{taxonomy_html()}
</section>

<section id="datasets">
<h2><span class="no">3.</span>Datasets</h2>
<p class="summary">Counts are tied to the linked source — verify the version before using it in a paper.</p>
{datasets_html(datasets)}
<h3>Notes</h3>
{notes_html(datasets)}
</section>

<section id="trends">
<h2><span class="no">4.</span>Publication trends</h2>
<p class="summary">Papers per year, computed automatically from <code>data/papers.yaml</code>.</p>
{trend_svg_html()}
</section>
</main>

<footer>
<p>Generated automatically from <code>data/papers.yaml</code> and <code>data/datasets.yaml</code> by <code>scripts/generate_site.py</code> · Last verified {esc(last_verified)}</p>
<h3>Cite this resource</h3>
<pre class="cite">{esc(cite)}</pre>
<div class="footer-links">
<a href="{REPO_URL}">GitHub repository</a>
<a href="{REPO_URL}/blob/main/README.md">README</a>
<a href="docs/papers.md">Papers</a>
<a href="docs/datasets.md">Datasets</a>
<a href="docs/taxonomy.md">Taxonomy</a>
<a href="docs/evaluation.md">Evaluation</a>
<a href="leaderboards/README.md">Leaderboards</a>
</div>
</footer>
</div>
<script>
const input = document.getElementById('search');
const counter = document.getElementById('counter');
function visible(tr) {{ return tr.style.display !== 'none'; }}
function apply() {{
  const q = input.value.trim().toLowerCase();
  let shown = 0;
  document.querySelectorAll('tbody tr').forEach(tr => {{
    const hit = tr.textContent.toLowerCase().includes(q);
    tr.style.display = hit ? '' : 'none';
    if (hit) shown++;
  }});
  document.querySelectorAll('section[data-group]').forEach(sec => {{
    const any = [...sec.querySelectorAll('tbody tr')].some(visible);
    sec.style.display = any ? '' : 'none';
  }});
  const papersBlock = document.getElementById('papers');
  const taxBlock = document.getElementById('taxonomy');
  const dataBlock = document.getElementById('datasets');
  papersBlock.style.display = [...document.querySelectorAll('section[data-group]')].some(s => s.style.display !== 'none') ? '' : 'none';
  taxBlock.style.display = [...document.querySelectorAll('#taxonomy-table tbody tr')].some(visible) ? '' : 'none';
  dataBlock.style.display = [...document.querySelectorAll('#datasets-table tbody tr')].some(visible) ? '' : 'none';
  counter.textContent = q ? shown + ' matching rows' : '';
}}
input.addEventListener('input', apply);

// active-section highlighting for the sticky nav
const navLinks = [...document.querySelectorAll('.nav-links a[href^="#"]')];
const sections = navLinks.map(a => document.querySelector(a.getAttribute('href'))).filter(Boolean);
const observer = new IntersectionObserver(entries => {{
  entries.forEach(entry => {{
    if (entry.isIntersecting) {{
      navLinks.forEach(a => a.classList.toggle('active', a.getAttribute('href') === '#' + entry.target.id));
    }}
  }});
}}, {{ rootMargin: '-45% 0px -50% 0px', threshold: 0 }});
sections.forEach(s => observer.observe(s));
</script>
</body>
</html>
"""


def robots_txt():
    return (
        "User-agent: *\n"
        "Allow: /\n"
        "\n"
        f"Sitemap: {RAW}/sitemap.xml\n"
    )


def sitemap_xml():
    pages = [
        "",
        "blob/main/README.md",
        "blob/main/CONTRIBUTING.md",
        "blob/main/docs/papers.md",
        "blob/main/docs/datasets.md",
        "blob/main/docs/taxonomy.md",
        "blob/main/docs/evaluation.md",
        "blob/main/docs/foundation_models.md",
        "blob/main/docs/open_problems.md",
        "blob/main/leaderboards/README.md",
    ]
    urls = "\n".join(f"  <url><loc>{REPO_URL}/{p}</loc></url>" if p else f"  <url><loc>{REPO_URL}</loc></url>" for p in pages)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    with open(ROOT / "data" / "papers.yaml", "r", encoding="utf-8") as f:
        papers = yaml.safe_load(f)["papers"]
    with open(ROOT / "data" / "datasets.yaml", "r", encoding="utf-8") as f:
        datasets = yaml.safe_load(f)["datasets"]
    outputs = {OUT: render(papers, datasets), ROBOTS: robots_txt(), SITEMAP: sitemap_xml()}
    if args.check:
        bad = []
        for path, content in outputs.items():
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                bad.append(str(path.relative_to(ROOT)))
        if bad:
            raise SystemExit("Generated files are stale: " + ", ".join(bad))
        print("Index page, robots.txt and sitemap.xml are up to date")
    else:
        for path, content in outputs.items():
            path.write_text(content, encoding="utf-8")
            print("wrote", path.relative_to(ROOT))


if __name__ == "__main__":
    main()
