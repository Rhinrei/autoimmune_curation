import argparse
import json
import os
import re

from typing import Dict, Iterable, List, Any

import spacy
from spacy.tokens import Doc, Span


def _read_jsonl(path: str) -> Iterable[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


POSITIVE_CUES = re.compile(
    r"\b(associate|associated|correlat|link|linked|induce|induced|trigger|cause|caused|risk|increase|elevated)\b",
    re.IGNORECASE,
)
NEGATION_CUES = re.compile(
    r"\b(no|not|failed|fails|absence|absent|without|did not|lack)\b", re.IGNORECASE
)
HEDGE_CUES = re.compile(r"\b(may|might|suggest|possible|potential)\b", re.IGNORECASE)


def _pairs(chemicals: List[str], diseases: List[str]) -> List[Dict[str, str]]:
    return [
        {"chemical": chem, "disease": dis}
        for chem in chemicals
        for dis in diseases
    ]


def _doc_sentences(doc: Doc) -> Iterable[Span]:
    for sent in doc.sents:
        yield sent


def _score_row(
    chemicals: List[str], diseases: List[str], pairs: List[Dict[str, str]], sentence: str
) -> float:
    score = 0.0
    if chemicals:
        score += 1
    if diseases:
        score += 1
    if pairs:
        score += 2
        score += min(len(pairs), 3)

    if POSITIVE_CUES.search(sentence):
        score += 1
    if NEGATION_CUES.search(sentence):
        score -= 1
    if HEDGE_CUES.search(sentence):
        score -= 0.5

    return score


def _polarity(sentence: str) -> str:
    if NEGATION_CUES.search(sentence):
        return "negative"
    if HEDGE_CUES.search(sentence):
        return "speculative"
    if POSITIVE_CUES.search(sentence):
        return "positive"
    return "unknown"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract sentence-level chemical-disease candidates with spaCy/scispaCy."
    )
    parser.add_argument("--in", dest="in_path", required=True, help="Input JSONL.")
    parser.add_argument("--out", required=True, help="Output JSONL.")
    parser.add_argument(
        "--model",
        default="en_ner_bc5cdr_md",
        help="spaCy model name (default: en_ner_bc5cdr_md).",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print a brief summary after processing.",
    )

    args = parser.parse_args()

    nlp = spacy.load(args.model)
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)

    total_sentences = 0
    sentences_with_entities = 0
    sentences_with_pairs = 0
    polarity_counts: Dict[str, int] = {}
    score_min: float | None = None
    score_max: float | None = None

    with open(args.out, "w", encoding="utf-8") as handle:
        for record in _read_jsonl(args.in_path):
            text = " ".join(
                part for part in [record.get("title"), record.get("abstract")] if part
            )
            if not text:
                continue
            doc = nlp(text)
            for sent in _doc_sentences(doc):
                chemicals = [
                    ent.text for ent in sent.ents if ent.label_ == "CHEMICAL"
                ]
                diseases = [ent.text for ent in sent.ents if ent.label_ == "DISEASE"]
                chem_list = sorted(set(chemicals))
                disease_list = sorted(set(diseases))
                pairs = _pairs(chem_list, disease_list)
                sentence = sent.text
                out: Dict[str, Any] = {
                    "pmid": record.get("pmid"),
                    "sentence": sentence,
                    "chemicals": chem_list,
                    "diseases": disease_list,
                    "pairs": pairs,
                }
                out["score"] = _score_row(
                    chem_list, disease_list, pairs, sentence
                )
                out["polarity_guess"] = _polarity(sentence)
                handle.write(json.dumps(out, ensure_ascii=False) + "\n")

                total_sentences += 1
                if chem_list or disease_list:
                    sentences_with_entities += 1
                if pairs:
                    sentences_with_pairs += 1
                polarity = out["polarity_guess"]
                polarity_counts[polarity] = polarity_counts.get(polarity, 0) + 1
                score = out["score"]
                score_min = score if score_min is None else min(score_min, score)
                score_max = score if score_max is None else max(score_max, score)

    if args.summary:
        print(f"Total sentences: {total_sentences}")
        print(f"Sentences with any entities: {sentences_with_entities}")
        print(f"Sentences with pairs: {sentences_with_pairs}")
        if score_min is not None and score_max is not None:
            print(f"Score range: {score_min} .. {score_max}")
        if polarity_counts:
            print("Polarity counts:")
            for key in sorted(polarity_counts.keys()):
                print(f"  {key}: {polarity_counts[key]}")


if __name__ == "__main__":
    main()
