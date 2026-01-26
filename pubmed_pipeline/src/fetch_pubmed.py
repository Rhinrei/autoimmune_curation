import argparse
import json
import os
import time
import xml.etree.ElementTree as ET

import requests
from typing import Dict, Iterable, List, Optional

EUTILS_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
DEFAULT_RETMAX = 50
DEFAULT_CHUNK_SIZE = 200


def _env_or_arg(value: Optional[str], env_name: str) -> Optional[str]:
    if value:
        return value
    return os.getenv(env_name)


def _read_pmids(path: str) -> List[str]:
    pmids = []
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            cleaned = line.strip()
            if cleaned:
                pmids.append(cleaned)
    return pmids


def _unique(pmids: List[str]) -> List[str]:
    seen = set()
    ordered = []
    for pmid in pmids:
        if pmid in seen:
            continue
        seen.add(pmid)
        ordered.append(pmid)
    return ordered


def _chunked(items: List[str], size: int) -> Iterable[List[str]]:
    for i in range(0, len(items), size):
        yield items[i : i + size]


def _esearch(
    query: str, retmax: int, email: str, api_key: Optional[str]
) -> List[str]:
    params: Dict[str, str] = {
        "db": "pubmed",
        "term": query,
        "retmax": str(retmax),
        "retmode": "json",
        "email": email,
    }
    if api_key:
        params["api_key"] = api_key
    response = requests.get(f"{EUTILS_BASE}/esearch.fcgi", params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    return data.get("esearchresult", {}).get("idlist", [])


def _extract_abstract(article: ET.Element) -> str:
    abstract_parts = []
    for elem in article.findall(".//Article/Abstract/AbstractText"):
        text = (elem.text or "").strip()
        label = elem.attrib.get("Label")
        if label:
            abstract_parts.append(f"{label}: {text}")
        else:
            abstract_parts.append(text)
    return " ".join(part for part in abstract_parts if part)


def _efetch(
    pmids: List[str], email: str, api_key: Optional[str]
) -> List[Dict[str, str]]:
    params: Dict[str, str] = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml",
        "email": email,
    }
    if api_key:
        params["api_key"] = api_key
    response = requests.get(f"{EUTILS_BASE}/efetch.fcgi", params=params, timeout=60)
    response.raise_for_status()
    root = ET.fromstring(response.text)
    records = []
    for article in root.findall(".//PubmedArticle"):
        pmid = article.findtext(".//MedlineCitation/PMID") or ""
        title = article.findtext(".//Article/ArticleTitle") or ""
        abstract = _extract_abstract(article)
        records.append(
            {
                "pmid": pmid,
                "title": title.strip(),
                "abstract": abstract.strip(),
            }
        )
    return records


def fetch_records(
    pmids: List[str],
    email: str,
    api_key: Optional[str],
    chunk_size: int,
    throttle_seconds: float,
) -> Iterable[Dict[str, str]]:
    for chunk in _chunked(pmids, chunk_size):
        records = _efetch(chunk, email, api_key)
        for record in records:
            yield record
        time.sleep(throttle_seconds)


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fetch PubMed abstracts by PMID list or search query."
    )
    parser.add_argument(
        "--pmids",
        help="Path to a text file with one PMID per line.",
    )
    parser.add_argument("--query", help="PubMed query string for esearch.")
    parser.add_argument("--retmax", type=int, default=DEFAULT_RETMAX)
    parser.add_argument("--out", required=True, help="Output JSONL file path.")
    parser.add_argument("--email", help="Email for NCBI usage policy.")
    parser.add_argument("--api-key", help="NCBI API key to increase rate limits.")
    parser.add_argument("--chunk-size", type=int, default=DEFAULT_CHUNK_SIZE)
    parser.add_argument("--throttle", type=float, default=0.35)
    return parser


def _collect_pmids(
    pmids_path: Optional[str],
    query: Optional[str],
    retmax: int,
    email: str,
    api_key: Optional[str],
) -> List[str]:
    pmids: List[str] = []
    if pmids_path:
        pmids.extend(_read_pmids(pmids_path))
    if query:
        pmids.extend(_esearch(query, retmax, email, api_key))
    pmids = _unique(pmids)
    if not pmids:
        raise SystemExit("No PMIDs found for the given input.")
    return pmids


def _write_abstracts(
    out_path: str,
    pmids: List[str],
    email: str,
    api_key: Optional[str],
    chunk_size: int,
    throttle_seconds: float,
) -> None:
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as handle:
        for record in fetch_records(pmids, email, api_key, chunk_size, throttle_seconds):
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def main() -> None:
    args = _build_arg_parser().parse_args()
    email = _env_or_arg(args.email, "NCBI_EMAIL")
    api_key = _env_or_arg(args.api_key, "NCBI_API_KEY")

    if not email:
        raise SystemExit("Missing --email or NCBI_EMAIL environment variable.")

    pmids = _collect_pmids(args.pmids, args.query, args.retmax, email, api_key)
    _write_abstracts(args.out, pmids, email, api_key, args.chunk_size, args.throttle)
    print(f"Wrote {len(pmids)} records to {args.out}")


if __name__ == "__main__":
    main()
