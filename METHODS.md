# Methods and limits

## Design

Forty frozen questions cover two tasks. Questions 1–20 concern historical withdrawals and warnings. Questions 21–40 concern comparative clinical QT evidence. Each task has five drug families and four questions per family. Questions within a family share sources and are correlated. The selected tasks do not represent all of medicine.

Use `dataset.json` for the included settings and counts. Direct requests contain the benchmark prompt, including any supplied source identifiers, without retrieval tools or source passages. Exact recorded direct message arrays are supplied. The evidence cutoff in the wrapper is 29 October 2026. Five direct slots were carried from the preceding configuration. This is a preserved run record, not a claim that all calls were a uniform fresh rerun.

`run_settings.json` gives model identifiers, recorded provider routes, sampling controls and bounds. Santé and base Ling share the stated provider and temperature/default-reasoning policy. Comparator settings differ, including provider-default sampling for Kimi. No served weight revision or sampling seed is established. Recorded aliases may later resolve differently.

## Grades and scores

The first AI judge assigned each frozen required facet C (fully correct), P (partly correct), I (incorrect) or N (not addressed). The exact first-judge model/version is not established. A later user-submitted targeted spot check supplied a small set of revised labels; its reviewer was unnamed and expertise/independence were not attested. Gemini judging has not been performed.

The original view uses all first AI labels. The current view replaces only listed facet grades with the returned labels after checking the original grade and answer hash. Unchecked facets, granular claim annotations and confidence remain first AI judgments. The return is not a representative agreement sample, a full human-label lock or approval of public wording.

Strict score per available answer is 100 × C / number of required facets. Questions receive equal weight. Partial grades have zero strict credit. This is required-facet coverage, not the fraction of all medical claims that are true. Raw facet pooling would weight questions differently and is not the displayed score.

Missing outputs remain null and unscored. Available-answer means exclude them. A separate delivered-credit sensitivity gives missing slots zero delivered credit; it does not change their scientific grade. Partial and format-failed displayed answers remain in the available-text analysis. Status does not establish scientific correctness.

Pair comparisons use questions with available text for both primary models. Six-model tables use questions available for all six in the given setting. Denominators can differ. The report also supplies half-credit-for-P, completed-only and family-level sensitivity views. A completed-only filter can select easier outputs and is not the headline analysis.

## Statistical interpretation

The analysis is exploratory and outcome-informed. Both tasks and all ten families remain included. The 95% percentile intervals resample whole families 10,000 times with seed 20261108. Five selected families per task give weak population support. Family sign-flip tests enumerate all 32 sign patterns under a symmetry assumption; model assignment was not randomized. The original two clinical-setting tests had Holm-adjusted values of 1.000. A released subset does not create a new test family.

The current direct clinical gap is +3.70 percentage points, driven by Q36 and Q37. Their decisive facets were not in the returned spot check. Its family interval touches zero and its two-sided family-test p value is 0.500. Do not infer superiority, equivalence or a lower harm rate. Fewer incorrect facets can coexist with more omissions. The preserved full evaluation also contains assisted results; they are not part of the direct-only release.

## Claim and source limits

Granular records use heterogeneous schemas, nested spans and repeated occurrences. Do not pool them into a supported-claim rate, fabricated-citation rate or source recall without defining eligible units and resolving source status. Per-answer fields retain the first reviewer's historical calculations and limits; their presence is not a validated aggregate metric.

The source register distinguishes required references from actual supplied evidence. It contains identifiers, versions, locators and reviewer-authored summaries, not full articles. A live URL can serve a later version. An unresolved identity or inaccessible full text remains a gap. A real identifier assigned to the wrong paper is not automatically a fabricated paper.

This package supports offline arithmetic and evidence inspection. It does not constitute clinical validation, medical advice or permission to reuse third-party content without checking its terms.
