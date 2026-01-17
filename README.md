Project Summary

Manual Curation and Validation of Chemical–Disease Relations in Autoimmune Disorders

In this project, I performed a focused manual curation of automatically extracted CHEMICAL–DISEASE relations from biomedical literature, with an emphasis on autoimmune and immune-mediated diseases (e.g. multiple sclerosis, lupus, sarcoidosis, autoimmune diabetes).

The goal was to evaluate the biological validity, specificity, and evidence strength of extracted relations and to distinguish true disease-relevant associations from experimental artifacts, background knowledge, or unsupported hypotheses.

Scope of Work
1. Relation validation

Each candidate relation was manually reviewed at the abstract level and classified as:

TRUE — supported by explicit experimental, clinical, or epidemiological evidence

FALSE — unsupported, overly general, or representing non-annotatable contexts

Special attention was paid to negative evidence, which was explicitly preserved rather than discarded.

2. Evidence-aware annotation

For each evaluated relation, I annotated:

Polarity

positive (asserted association)

negative (explicitly disproven)

speculative (hypothesis-level statements)

ManualConfidence
Reflecting author commitment, based on:

language (e.g. may, suggests vs induces, results in)

study type (case report, cohort, animal model)

reproducibility and specificity

EvidenceSentence
A minimal, self-contained sentence supporting (or refuting) the relation.

3. Differentiation of relation types

I consistently distinguished between:

Valid disease markers or mechanisms

e.g. GD1a antibodies in multiple sclerosis

myo-inositol as a marker of gliosis in chronic MS lesions

HgCl₂ inducing autoimmune disease in animal models

Non-annotatable contexts, including:

experimental triggers or positive controls (e.g. cyclophosphamide, pristane)

therapeutic or tolerizing interventions (e.g. DNA vaccines, peptides)

diagnostic or imaging agents (e.g. gadolinium)

routine clinical or metabolic parameters (e.g. cholesterol, bilirubin, creatine)

general review statements or hypothesis-only papers

4. Ontology and identifier control

I validated entity identifiers (MeSH) and avoided incorrect mappings by:

preferring parent MeSH terms when specific molecular variants lacked descriptors

excluding entities whose identifiers corresponded to unrelated concepts

This ensured ontology consistency and downstream usability.