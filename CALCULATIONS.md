# Calculation guide

## Question and evidence

How should a small learning experiment report its outcomes?

Synthetic assignment records with baseline, follow-up and missing-outcome indicators.

**Status:** SYNTHETIC / RULE-BASED PROTOTYPE | no educational validity claim.

## Design

Analyze observed outcomes by assigned group; retain attrition, baseline imbalance, standardized effects and bootstrap uncertainty.

## Calculation and interpretation

`Cohen d = (mean treatment - mean control)/pooled sample SD.`

Complete-case analysis by assignment is not a full intention-to-treat estimate when outcomes are missing. Observational assignment and attrition can undermine causal claims even when a mean difference is precise.

## Evidence table

Worked example — illustrative, not a measured research result. Full precision below is for traceability, not a claim of measurement precision.

| Quantity | Value | Unit / meaning | JSON path |
|---|---:|---|---|
| Cohen d: [2,3,4] vs [1,2,3] | 1.0 | unitless | `outputs.Cohen d: [2,3,4] vs [1,2,3]` |
| raw mean difference | 1 | unitless | `outputs.raw mean difference` |

Source: [results/review_examples.json](results/review_examples.json). Values resolve directly from this file when figures are regenerated.

This experiment-analysis prototype keeps assignment, baseline measures, follow-up outcomes, and attrition in one inspectable record. It reports group differences, pooled-SD effect sizes, and bootstrap intervals while flagging sparse groups and baseline imbalance. Missing outcomes are handled as complete cases grouped by assignment, so the documentation explicitly limits causal interpretation and avoids calling the analysis a complete intention-to-treat estimate.

## Verification performed in this review

25 existing unittest checks passed. The bundled demonstration executed successfully in this review.

The figure-generation check verifies agreement between the selected source values and SVGs. It does not validate the raw dataset, fitted model, identification assumptions, or external generalization.

```bash
python scripts/build_review_figures.py
python scripts/build_review_figures.py --check
```

For the explicitly illustrative example:

```bash
python scripts/review_examples.py
```

## Implementation map

Follow these functions to inspect each transformation. Validation helpers and private functions remain visible in the linked modules.

| Function | Purpose / documented behavior |
|---|---|
| [`mean`](src/learning_experiment_platform/core.py#L26) | Inspect the explicit implementation and its callers. |
| [`assign`](src/learning_experiment_platform/core.py#L31) | Assign unique participant IDs to two groups with size difference <= 1. |
| [`gain`](src/learning_experiment_platform/core.py#L54) | Return paired post-minus-pre change scores. |
| [`cohens_d`](src/learning_experiment_platform/core.py#L73) | Return pooled-SD Cohen d for two independent groups. |
| [`bootstrap_mean_difference_ci`](src/learning_experiment_platform/core.py#L119) | Percentile bootstrap CI for treatment-minus-control mean difference. |
| [`experiment_record`](src/learning_experiment_platform/core.py#L162) | Create a compact, serializable analysis record for a planned experiment. |
| [`analyze_experiment`](src/learning_experiment_platform/core.py#L277) | Analyze pre/post outcomes by assigned group with transparent safeguards. |

## What remains before a stronger research claim

Complete-case analysis by assignment is not a full intention-to-treat estimate when outcomes are missing. Observational assignment and attrition can undermine causal claims even when a mean difference is precise. A successful software test is not validation of a scientific construct. New experiments should state their split unit, comparator, outcome, uncertainty procedure and failure criteria before examining final test results.
