# Reproduced results

Current view: submitted labels applied only to their specified facets. Other labels remain first AI judgments. Original results are retained in results.json. These are exploratory coverage scores, not clinical accuracy.

| Model | Setting | Available / scheduled | Strict C | Delivered C |
| --- | --- | --- | --- | --- |
| DeepSeek | direct | 40 / 40 | 17.71% | 17.71% |
| Base Ling | direct | 40 / 40 | 13.33% | 13.33% |
| Santé | direct | 37 / 40 | 13.96% | 12.92% |
| Mistral | direct | 40 / 40 | 6.67% | 6.67% |
| Kimi | direct | 40 / 40 | 12.50% | 12.50% |
| Qwen | direct | 40 / 40 | 9.58% | 9.58% |

## Matched Santé and base Ling

| Setting | Task | Pairs | Santé C | Ling C | Gap, pp | Family-bootstrap interval, pp |
| --- | --- | --- | --- | --- | --- | --- |
| direct | Historical | 19 | 11.40% | 14.47% | -3.07 | -7.02 to +0.93 |
| direct | Clinical | 18 | 16.67% | 12.96% | +3.70 | +0.00 to +7.84 |

Intervals resample whole families (10,000 draws, seed 20261108); five selected families per task. They are descriptive and do not establish superiority or equivalence.

## Common-question comparison

| Model | Setting | Task | Common questions | Strict C | Answers with at least one I |
| --- | --- | --- | --- | --- | --- |
| DeepSeek | direct | Historical | 19 | 20.18% | 8 |
| Base Ling | direct | Historical | 19 | 14.47% | 10 |
| Santé | direct | Historical | 19 | 11.40% | 8 |
| Mistral | direct | Historical | 19 | 5.26% | 18 |
| Kimi | direct | Historical | 19 | 9.65% | 17 |
| Qwen | direct | Historical | 19 | 9.65% | 16 |
| DeepSeek | direct | Clinical | 18 | 16.67% | 13 |
| Base Ling | direct | Clinical | 18 | 12.96% | 11 |
| Santé | direct | Clinical | 18 | 16.67% | 8 |
| Mistral | direct | Clinical | 18 | 9.26% | 16 |
| Kimi | direct | Clinical | 18 | 16.20% | 13 |
| Qwen | direct | Clinical | 18 | 11.11% | 14 |

## Clinical family sign-flip sensitivity

- direct: two-sided p = 0.500; 2 nonzero families of 5.

The full study considered two clinical setting tests; its Holm-adjusted values were both 1.000. The direct-only subset does not redefine that testing family. No significance claim is made.

The current direct clinical gap depends on Q36 and Q37; those decisive facets were not in the returned review. Other-model labels remain AI grades.
