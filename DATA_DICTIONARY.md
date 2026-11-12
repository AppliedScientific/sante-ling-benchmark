# Data dictionary

| File | Unit and purpose |
| --- | --- |
| `dataset.json` | Included settings, counts, exclusions and provenance hash |
| `data/answers.json` | One scheduled slot; named model, question, setting, status, exact text or null, text hash, original facet vector, confidence and first-review reason |
| `data/questions.json` | Forty exact prompts; source cutoff, jurisdiction, family, required facet/source contracts and accepted reviewer-authored definitions |
| `data/run_settings.json` | Model/provider identifiers, limits, sampling policy and explicit unknowns |
| `data/request_inventory.json` | Recorded direct messages and hashes; in the company edition, supplied-source metadata and stop records for assisted slots |
| `data/source_register.json` | Required source identifiers, versions, locators and access limits |
| `data/assessment_sources.json` | Question-specific evidence-key legends and reviewer-authored source summaries used by granular assessments |
| `data/returned_review.json` | Submitted facet decisions, source notes and reasons; independent of original labels |
| `assessments/question-NN.json` | Original answer-specific scientific claim and citation records for the included answers only |
| `results/results.json` | Original and current descriptive analyses, family sensitivities and common-question comparisons |

IDs have the form `Q30-M1-direct`: question 30, model 1, direct setting. M1 is Santé; M2 base Ling; M3 Kimi; M4 DeepSeek; M5 Qwen; M6 Mistral. These are package-local named IDs, not a distributed private blinding key. Facet order is given by `facet_ids`. The first AI reason/confidence does not describe a later returned grade.

Text hashes use SHA-256 over UTF-8. Annotation spans use Python Unicode code points, zero-based and end-exclusive. Nested spans can repeat a phrase. Message hashes use JSON with sorted keys and `ensure_ascii=False`, as recorded. Source hashes identify retained representations where provided; they do not guarantee recovery from today's URL.

Original annotation vocabularies and unresolved flags are retained. A few historical references are explicitly marked omitted in the source export. Supplemental source-key maps remove private workspace links and identify that omission. Exact answer text and its annotation records are unchanged. Required source recall is not inferred from a minimum list of source contributions.

No patient records, credentials, account balances or private crosswalk are included. The prompts are literature questions. Generated answers can contain scientific errors; the assessments are evidence for review, not instructions for care.
