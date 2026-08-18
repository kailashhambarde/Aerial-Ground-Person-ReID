from pathlib import Path
from urllib.parse import urlparse
import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def valid_url(value):
    if value is None:
        return True
    p = urlparse(str(value))
    return p.scheme in {"http", "https"} and bool(p.netloc)


def main():
    papers = load_yaml(ROOT / "data" / "papers.yaml")["papers"]
    datasets = load_yaml(ROOT / "data" / "datasets.yaml")["datasets"]

    paper_ids = [p["id"] for p in papers]
    if len(paper_ids) != len(set(paper_ids)):
        raise SystemExit("Duplicate paper id detected")

    dataset_names = [d["name"] for d in datasets]
    if len(dataset_names) != len(set(dataset_names)):
        raise SystemExit("Duplicate dataset name detected")

    required_paper = {"id", "method", "year", "venue", "title", "task", "categories", "paper", "status", "verified_on"}
    for p in papers:
        missing = required_paper - set(p)
        if missing:
            raise SystemExit(f"Paper {p.get('id')} missing: {sorted(missing)}")
        for field in ("paper", "code"):
            if not valid_url(p.get(field)):
                raise SystemExit(f"Invalid URL in {p['id']}:{field}")

    required_dataset = {"name", "year", "identities", "platforms", "modalities", "video", "source"}
    for d in datasets:
        missing = required_dataset - set(d)
        if missing:
            raise SystemExit(f"Dataset {d.get('name')} missing: {sorted(missing)}")
        if not valid_url(d.get("source")):
            raise SystemExit(f"Invalid source URL for dataset {d['name']}")

    print(f"OK: {len(papers)} papers, {len(datasets)} datasets")


if __name__ == "__main__":
    main()
