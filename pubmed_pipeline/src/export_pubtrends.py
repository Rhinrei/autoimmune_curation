import argparse
import csv
import os
from typing import Dict, Iterable, Any

from io_utils import read_jsonl


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export candidate relations in a PubTrends-like CSV format."
    )
    parser.add_argument("--in", dest="in_path", required=True, help="Input JSONL.")
    parser.add_argument("--out", required=True, help="Output CSV file.")
    parser.add_argument(
        "--include-no-pairs",
        action="store_true",
        help="Include rows without explicit chemical-disease pairs.",
    )
    args = parser.parse_args()

    fieldnames = [
        "pmid",
        "chemical",
        "disease",
        "evidence_sentence",
        "polarity_guess",
        "score",
        "chemical_norm_id",
        "disease_norm_id",
        "manual_label",
        "manual_confidence",
        "error_type",
    ]

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()

        for row in read_jsonl(args.in_path):
            pairs = row.get("pairs") or []
            if not pairs and not args.include_no_pairs:
                continue
            if not pairs:
                pairs = [{"chemical": "", "disease": ""}]
            for pair in pairs:
                writer.writerow(
                    {
                        "pmid": row.get("pmid"),
                        "chemical": pair.get("chemical", ""),
                        "disease": pair.get("disease", ""),
                        "evidence_sentence": row.get("sentence", ""),
                        "polarity_guess": row.get("polarity_guess", "unknown"),
                        "score": row.get("score"),
                        "chemical_norm_id": "",
                        "disease_norm_id": "",
                        "manual_label": "",
                        "manual_confidence": "",
                        "error_type": "",
                    }
                )


if __name__ == "__main__":
    main()
