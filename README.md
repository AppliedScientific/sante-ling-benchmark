# Santé and Ling: direct-model evidence benchmark

A small data and analysis repository for inspecting one recorded scientific-literature evaluation. This private preparation copy can be considered for public release after the owners approve its wording and reuse terms. No public release is implied.

**Scope:** 40 questions × six models × one direct setting = 240 scheduled outputs. There are 237 exact displayed answers and three missing Santé outputs. No retrieval-assisted run, private orchestration code, development history, improvement brief or editorial draft is included. The data are displayed-output records, not raw provider wire envelopes.

The questions cover historical drug withdrawals/warnings and comparative clinical QT evidence. The models are Santé, base Ling, Kimi, DeepSeek, Qwen and Mistral. Exact identifiers, providers and recorded settings are in [run settings](data/run_settings.json).

## Start here

- [Reproduced results](results/TABLES.md).
- [Methods and limits](METHODS.md), [data dictionary](DATA_DICTIONARY.md) and [reuse status](REUSE.md).
- [Every answer and missing record](data/answers.json), [exact questions and rubric](data/questions.json), and [recorded direct requests](data/request_inventory.json).
- [All 237 answer-specific claim/citation assessments](assessments), [assessment source-key maps](data/assessment_sources.json) and [source identities/locators](data/source_register.json).
- [Five returned spot-check criteria](data/returned_review.json). Three differ from the first AI grades. This is a targeted subset, not full human validation.

On the same 18 direct clinical questions, Santé and DeepSeek both have 16.67% strict required-facet coverage; base Ling has 12.96%. On 19 matched historical questions, base Ling has 14.47% and Santé 11.40%. These are descriptive results with unequal review depth. The direct clinical gap depends on Q36 and Q37, whose decisive grades were not checked in the returned review. No statistically significant superiority or clinical safety claim is established.

## Reproduce without keys

Python 3.10 or later; standard library only. No installation, model call or network access is needed.

```sh
python3 verify.py
python3 analysis.py --output /tmp/sante-ling-check
```

The second command reproduces the result JSON and tables in a separate folder. As a worked example, the direct clinical row in `TABLES.md` comes from the 18 questions for which every model has displayed text. For each answer calculate C / number of required facets, then average the 18 fractions. `verify.py` compares the regenerated files byte for byte with `results/`.

Original answers, missing records and first AI labels stay unchanged. Returned labels are a separate analysis view. Endpoint aliases and current web pages do not guarantee the same served weights or frozen source versions. The [dataset manifest](dataset.json) and [checksums](SHA256SUMS) identify this release candidate.
