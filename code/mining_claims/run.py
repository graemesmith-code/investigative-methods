"""Offline runner. Fixture mode demonstrates arithmetic, not live monitoring."""
import argparse
import json
from pathlib import Path
from compare import assess

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1] / "research/2026-10-12/mining-claims"


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--observations", type=Path, default=HERE / "fixtures/observations.json")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    envelope = load_json(args.observations)
    manifest = {s["source_id"]: s for s in load_json(RESEARCH / "source-manifest.json")}
    cases = [load_json(p) for p in sorted((HERE / "cases").glob("*.json"))]
    observations = {o["case_id"]: o for o in envelope["observations"]}
    results = [assess(c, observations.get(c["id"], {}), manifest) for c in cases]
    payload = {"mode": envelope["mode"], "warning": "No finding of intentional misstatement. Source and scope review remains necessary.", "results": results}
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 2 if any(r["status"] == "blocked" for r in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
