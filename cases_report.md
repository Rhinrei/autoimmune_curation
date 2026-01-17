# Case-based report: manual validation of Chemical-Disease relations

This report summarizes representative cases reviewed during manual curation of
automatically extracted CHEMICAL-DISEASE relations related to autoimmune and
immune-mediated diseases.

The cases illustrate common success and failure modes of automated relation
extraction systems and highlight the necessity of expert biological judgement.

## Case 1: GD1a - Multiple Sclerosis  
**PMID:** 10618693 <br>
**Decision:** added to database  
**Relation type:** CHEMICAL-DISEASE: marker/mechanism  

Elevated IgG antibody titers against the ganglioside GD1a were observed more
frequently in patients with multiple sclerosis than in controls and were further
associated with disease severity. The authors explicitly identify GD1a-directed
immune responses as discriminative for MS.

## Case 2: Silicone (gel/oil) - Lupus
**PMID:** 10799447<br>
**Decision:** FALSE  
**Polarity:** negative  

In contrast to a positive control (pristane), silicone gel and silicone oil failed to
induce lupus-associated autoantibodies or lupus nephritis in animal models.

**Rationale:**  
This case represents explicit negative evidence. Immune activation without
disease induction was not annotated as a valid CHEMICAL-DISEASE relation.

## Case 3: Cyclophosphamide - Autoimmune Diabetes  
**PMID:** 10896769<br>
**Decision:** FALSE  

Cyclophosphamide accelerated autoimmune diabetes only in IL-10-deficient mice
and did not induce disease independently.

**Rationale:**  
Cyclophosphamide acts as an experimental trigger dependent on genetic context
rather than a general disease-causing agent and was therefore excluded.

## Case 4: Sulfatides - Multiple Sclerosis  
**PMID:** 10618693<br>
**Decision:** FALSE  

Increased IgM responses to sulfatides were observed in MS but also in other
inflammatory neurological conditions.

**Rationale:**  
Due to lack of disease specificity and discriminative value, sulfatides were not
annotated as MS markers.

## Case 5: Gangliosides - Diabetes-related salivary gland complications  
**PMID:** 10867739<br>
**Decision:** FALSE  

The abstract proposes a possible autoimmune role for gangliosides but provides
no experimental or observational evidence.

**Rationale:**  
Hypothesis-only and conceptual statements without supporting data were excluded
from structured annotation.

## Conclusions

Across reviewed cases, valid CHEMICAL-DISEASE relations required:
- disease-specific quantitative evidence
- explicit author interpretation
- sufficient specificity to distinguish from general immune activation

Relations based on experimental setup, therapeutic intervention, non-specific
markers, or hypothesis-level reasoning were consistently excluded.
