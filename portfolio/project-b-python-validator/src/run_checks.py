"""Read a CSV of registration records, validate each, write results + summary."""
import csv
import sys
from pathlib import Path

from validator import validate_record

ROOT = Path(__file__).resolve().parent.parent


def run(input_path: Path, output_path: Path) -> dict:
    with open(input_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    results = []
    for row in rows:
        errors = validate_record(row)
        results.append({
            "id": row["id"],
            "status": "FAIL" if errors else "PASS",
            "errors": ";".join(errors),
        })

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "status", "errors"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(results)

    passed = sum(r["status"] == "PASS" for r in results)
    return {"total": len(results), "passed": passed, "failed": len(results) - passed}


if __name__ == "__main__":
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data" / "sample_input.csv"
    dst = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "data" / "actual_output.csv"
    s = run(src, dst)
    print(f"Records: {s['total']} | Passed: {s['passed']} | Failed: {s['failed']}")
    print(f"Results written to {dst}")
