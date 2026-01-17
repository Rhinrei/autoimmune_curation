# Manual Curation of Chemical-Disease Relations in Autoimmune Disorders

This repository contains a small-scale manual curation project focused on validating
automatically extracted **CHEMICAL-DISEASE relations** from biomedical literature,
with an emphasis on autoimmune and immune-mediated diseases.

The project demonstrates evidence-aware biological data curation rather than
model development, with particular attention to false positives, weak evidence,
and experimental artifacts possibly produced by automated BioNLP pipelines.

## Source Dataset

The curated relations in this project are based on a subset of the **PubTrends relation extraction dataset**
(Release of **June 18, 2020**) https://lp.jetbrains.com/research/paper_analyzer/projects/.

## Project Motivation

Automated text-mining systems are highly effective at extracting candidate
chemical-disease relations, but often lack the ability to distinguish:

- disease-relevant biological associations  
- experimental or therapeutic interventions  
- hypothesis-level or review-only statements  
- negative or non-specific evidence  

The goal of this project was to manually evaluate such extracted relations
and convert them into biologically defensible structured knowledge.

## Scope of Work

### Manual validation of relations
Each candidate CHEMICAL-DISEASE relation was reviewed at the abstract level and
classified as either:

- **TRUE** — supported by explicit experimental, clinical, or epidemiological evidence  
- **FALSE** — unsupported, non-specific, or not suitable for structured annotation  

Negative evidence was explicitly preserved and annotated.

### Evidence-aware annotation fields

For each evaluated relation, the following fields were added:

- **ManualLabel**  
  TRUE or FALSE based on biological validity

- **Polarity**  
  - positive — asserted association  
  - negative — explicitly disproven  
  - speculative — hypothesis-level statements  

- **ManualConfidence**  
  Reflects the degree of commitment expressed by the authors, based on:
  - language (e.g. *may suggest* vs *induces*)
  - study type (case report, cohort, animal model)
  - specificity and reproducibility  

- **EvidenceSentence**  
  A minimal sentence directly supporting or refuting the relation

- **ErrorType** (for FALSE relations)  
  Used to characterize common failure modes of automated extraction

## Annotation Principles

### Annotated as valid relations
- Disease-specific biochemical or immunological markers  
- Experimentally demonstrated disease mechanisms  
- Reproducible animal models inducing autoimmune phenotypes  

### Explicitly excluded
- Therapeutic or tolerizing interventions (e.g. vaccines, peptides)  
- Experimental triggers or positive controls  
- Diagnostic or imaging agents  
- Routine clinical or metabolic parameters  
- General review statements without disease-specific evidence  
- Hypothesis-only or conceptual papers  


## Repository Structure

