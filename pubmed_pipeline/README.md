# PubMed Chemical-Disease Curation (Minimal Pipeline)

This folder contains a small Python pipeline to download PubMed abstracts,
extract CHEMICAL/DISEASE mentions, and generate candidate relations with
evidence sentences plus light polarity/score signals for manual curation.

## Project rationale

Automated BioNLP can surface candidate relations, but domain experts still need:
- a defensible evidence sentence,
- polarity (positive/negative/speculative),
- a compact, reviewable output format.

This pipeline focuses on those inputs for a lightweight curation workflow.

## Setup

```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
```

## Usage

Fetch by a list of PMIDs:

```bash
python src/fetch_pubmed.py --pmids data/sample_pmids.txt --email you@example.com --out data/abstracts.jsonl
```

Fetch by search query:

```bash
python src/fetch_pubmed.py --query "autoimmune disease[MeSH Terms] AND cytokine" --retmax 100 --email you@example.com --out data/abstracts.jsonl
```

## Candidate extraction (spaCy/scispaCy)

Install the biomedical NER model:

```bash
python -m pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.4/en_ner_bc5cdr_md-0.5.4.tar.gz
```

Run the extractor:

```bash
python src/extract_candidates_spacy.py --in data/abstracts.jsonl --out data/candidates_spacy.jsonl --model en_ner_bc5cdr_md
```

## Output schema

Each JSONL line represents one sentence:
- `pmid`, `sentence`
- `chemicals`, `diseases`
- `pairs` (all chemical-disease combinations in the sentence)
- `score` (light heuristic ranking)
- `polarity_guess` (positive/negative/speculative/unknown)

## PubTrends-style export

Export a CSV suitable for manual curation and downstream analysis:

```bash
python src/export_pubtrends.py --in data/candidates_spacy.jsonl --out data/curation_export.csv
```

Export columns include placeholders for normalization and manual labels:
`chemical_norm_id`, `disease_norm_id`, `manual_label`, `manual_confidence`, `error_type`.

## Annotation principles (compact)

Valid relations require explicit disease-relevant evidence, not just
therapeutic use, experimental triggers, or hypothesis-only statements.
Negative evidence should be preserved and marked as such.

## Error taxonomy (compact)

- therapeutic use (drug treats disease, not a mechanism/marker)
- experimental trigger/control (induces phenotype only as a model)
- non-specific marker (not disease-discriminative)
- hypothesis-only (no supporting data)
- off-target association (unrelated co-mention)

## Notes

- NCBI requests an email address for API usage; set `--email` or `NCBI_EMAIL`.
- You can also set `NCBI_API_KEY` in your environment to raise rate limits.
- Abstracts output: one JSON object per line with `pmid`, `title`, `abstract`.
