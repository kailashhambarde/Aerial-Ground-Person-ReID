from pathlib import Path
import argparse
import yaml

ROOT = Path(__file__).resolve().parents[1]

# task -> table section (same grouping as Awesome-Aerial-Ground-Object-Re-Identification)
GROUPS = [
    ("Image-based Person AG-ReID", {"image-ag-reid", "single-view-ag-reid", "text-ag-reid", "multimodal-ag-reid"}),
    ("Image-based Vehicle AG-ReID", {"image-vehicle-ag-reid"}),
    ("Video-based Person AG-ReID", {"video-ag-reid"}),
    ("Challenges & Workshops", {"challenge"}),
    ("More Related Exploration", {"related"}),
]

REPO = "https://github.com/kailashhambarde/Aerial-Ground-Person-ReID"


def load(path, key):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)[key]


def fmt_num(value):
    return f"{int(value):,}" if value else "—"


def fmt_list(values):
    return ", ".join(values) if values else "—"


def resources(p):
    parts = [f"[Paper]({p['paper']})"]
    if p.get("code"):
        parts.append(f"[Code]({p['code']})")
    if p.get("dataset_url"):
        parts.append(f"[Dataset]({p['dataset_url']})")
    return " · ".join(parts)


def method_cell(method):
    return f"**{method}**" if method and method != "—" else "—"


def group_papers(papers):
    by_task = {task: g for g, tasks in GROUPS for task in tasks}
    buckets = {g: [] for g, _ in GROUPS}
    for p in papers:
        task = p.get("task")
        if task not in by_task:
            raise SystemExit(f"Unknown task '{task}' for paper {p.get('id')} — add it to GROUPS in {__file__}")
        buckets[by_task[task]].append(p)
    return buckets


def papers_tables_md(papers):
    """Only the grouped paper tables (no doc header/footer) — used in docs/papers.md and README.md."""
    lines = []
    for g, _ in GROUPS:
        group = sorted(group_papers(papers)[g], key=lambda x: (-int(x["year"]), x["method"].lower()))
        if not group:
            continue
        lines += [f"### {g}", "", "| Conference / Journal | Method | Title | Resources |", "| :------------------- | :----- | :----- | :--------- |"]
        for p in group:
            venue = f"**{p['venue']} {p['year']}**"
            lines.append(f"| {venue} | {method_cell(p.get('method'))} | {p['title']} | {resources(p)} |")
        lines.append("")
    return "\n".join(lines)


def papers_md(papers):
    n = len(papers)
    with_code = sum(1 for p in papers if p.get("code"))
    peer = sum(1 for p in papers if p.get("status") == "peer-reviewed")
    preprints = sum(1 for p in papers if p.get("status") == "preprint")
    lines = [
        "# 📄 Papers",
        "",
        "> [!IMPORTANT]",
        "> **Generated file — edit [`data/papers.yaml`](../data/papers.yaml), not this table.**",
        "> Tables are rebuilt by [`scripts/generate_tables.py`](../scripts/generate_tables.py) (locally or by CI).",
        "",
        f"**{n} papers tracked** · **{with_code} with public code** · **{peer} peer-reviewed** · **{preprints} preprints**",
        "",
    ]
    lines.append(papers_tables_md(papers))
    lines += [
        "> [!TIP]",
        f"> Missing a paper or know of public code? Open a [paper issue]({REPO}/issues/new/choose) or follow [CONTRIBUTING.md](../CONTRIBUTING.md).",
        "",
    ]
    return "\n".join(lines) + "\n"


def datasets_table_md(datasets):
    """Only the datasets table + notes (no doc header) — used in docs/datasets.md and README.md."""
    lines = [
        "| Dataset | Year | Category | IDs | Scale | Platforms | Modalities | Video | Geometry | Download |",
        "| :------- | :---: | :-------- | ---: | :---- | :--------- | :--------- | :---: | :------- | :------- |",
    ]
    for d in sorted(datasets, key=lambda x: (int(x["year"]), x["name"].lower())):
        parts = []
        if d.get("images"):
            parts.append(f"{int(d['images']):,} images")
        if d.get("tracklets"):
            parts.append(f"{int(d['tracklets']):,} tracklets")
        if d.get("frames"):
            parts.append(f"{int(d['frames']):,} frames")
        if d.get("boxes"):
            parts.append(f"{int(d['boxes']):,} boxes")
        geom = []
        if d.get("altitude_m"):
            geom.append(f"alt. {d['altitude_m']} m")
        if d.get("distance_m"):
            geom.append(f"dist. {d['distance_m']} m")
        if d.get("geometry_note"):
            geom.append(d["geometry_note"])
        download = f"[download]({d['download']})" if d.get("download") else "—"
        lines.append(
            f"| [**{d['name']}**]({d['source']}) | {d['year']} | {d.get('category') or '—'} | {fmt_num(d.get('identities'))} | "
            f"{'; '.join(parts) or '—'} | {fmt_list(d.get('platforms'))} | {fmt_list(d.get('modalities'))} | "
            f"{'✓' if d.get('video') else '—'} | {'; '.join(geom) or '—'} | {download} |"
        )
    lines += ["", "**Notes**", ""]
    for d in sorted(datasets, key=lambda x: x["name"].lower()):
        if d.get("notes"):
            lines.append(f"- **{d['name']}**: {d['notes']}")
    return "\n".join(lines)


def datasets_md(datasets):
    n = len(datasets)
    total_ids = sum(int(d.get("identities") or 0) for d in datasets)
    video = sum(1 for d in datasets if d.get("video"))
    multimodal = sum(1 for d in datasets if len(d.get("modalities", []) or []) > 1)
    lines = [
        "# 🗃️ Datasets",
        "",
        "> [!IMPORTANT]",
        "> **Generated file — edit [`data/datasets.yaml`](../data/datasets.yaml), not this table.**",
        "> Counts are tied to the linked source; verify the dataset version before using it in a paper.",
        "",
        f"**{n} datasets catalogued** · **{total_ids:,} identities** · **{video} video benchmarks** · **{multimodal} multimodal benchmarks**",
        "",
    ]
    lines.append(datasets_table_md(datasets))
    lines += [
        "",
        "> [!TIP]",
        f"> Know a dataset that is missing or have corrections? Open a [paper issue]({REPO}/issues/new/choose) or follow [CONTRIBUTING.md](../CONTRIBUTING.md).",
        "",
    ]
    return "\n".join(lines) + "\n"


def apply_readme(papers, datasets):
    """Inject full tables into README.md between marker comments, keeping hand-written prose intact."""
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    blocks = {"PAPERS": papers_tables_md(papers).strip("\n"), "DATASETS": datasets_table_md(datasets).strip("\n")}
    for marker, block in blocks.items():
        start, end = f"<!-- {marker}:START -->", f"<!-- {marker}:END -->"
        if start not in text or end not in text:
            raise SystemExit(f"README.md is missing the {start} / {end} markers")
        pre, rest = text.split(start, 1)
        _, post = rest.split(end, 1)
        text = pre + start + "\n" + block + "\n" + end + post
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    papers = load(ROOT / "data" / "papers.yaml", "papers")
    datasets = load(ROOT / "data" / "datasets.yaml", "datasets")
    outputs = {
        ROOT / "docs" / "papers.md": papers_md(papers),
        ROOT / "docs" / "datasets.md": datasets_md(datasets),
        ROOT / "README.md": apply_readme(papers, datasets),
    }
    if args.check:
        bad = []
        for path, content in outputs.items():
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                bad.append(str(path.relative_to(ROOT)))
        if bad:
            raise SystemExit("Generated files are stale: " + ", ".join(bad))
        print("Generated tables are up to date")
    else:
        for path, content in outputs.items():
            path.write_text(content, encoding="utf-8")
            print("wrote", path.relative_to(ROOT))


if __name__ == "__main__":
    main()
