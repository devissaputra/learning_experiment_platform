# Research protocol

## Project

Learning Experiment Platform

## Research questions

1. What is the treatment-minus-control difference in the primary learning outcome?
2. How do baseline differences, gain scores, and standardized effects change the interpretation?
3. What uncertainty surrounds the observed mean difference?
4. How much attrition occurs in each assigned group, and is it differential?
5. Which protocol deviations or missing-data assumptions limit interpretation?

## Current baseline

The current implementation provides:

- seeded two-group random assignment
- compact experiment metadata records
- baseline group summaries
- paired post-minus-pre gains
- treatment-minus-control post and gain differences
- pooled-SD Cohen d
- percentile bootstrap confidence intervals for raw mean differences
- group-specific and overall attrition summaries
- transparent analysis flags

## Assignment

`assign()` shuffles unique participant IDs with a supplied seed and creates treatment/control groups whose sizes differ by at most one.

The seed supports reproducibility of the software assignment. A real experiment must still document recruitment, allocation concealment where relevant, timing, and who had access to the assignment.

## Analysis population

The integrated baseline stays grouped by **assigned group**.

For participants with missing post outcomes:

- assignment counts are preserved
- attrition is reported
- no outcome is imputed
- post and gain effects use observed cases only

This complete-case baseline is intentionally explicit. It is not a substitute for a pre-specified missing-data strategy or a full intention-to-treat analysis when outcomes are missing.

## Effect estimates

The implementation reports:

- baseline mean difference
- post-test mean difference
- gain-score mean difference
- Cohen d for baseline, post, and gains when estimable

If the pooled standard deviation is zero, Cohen d is reported as not estimable rather than as zero.

## Uncertainty

The baseline reports seeded percentile-bootstrap confidence intervals for the raw post-test and gain-score mean differences.

The current version does not provide p-values, model-based standard errors, cluster-robust inference, multiplicity adjustments, or confidence intervals for Cohen d.

## Attrition

Attrition is calculated from assigned participants without observed post outcomes. The system reports:

- counts by assigned group
- rates by assigned group
- overall attrition rate
- treatment-minus-control differential attrition rate

A configurable differential-attrition threshold produces a review flag. The flag is not a causal diagnosis.

## Analysis flags

The current review layer can surface:

- attrition present
- differential attrition requiring review
- a small observed group
- post effect not estimable
- gain effect not estimable
- baseline standardized difference requiring review

Thresholds are review prompts rather than universal experiment-quality rules.

## Pre-specification

`experiment_record()` creates serializable metadata for the hypothesis, primary outcome, assignment seed, exclusions, and analysis method.

For a real confirmatory study, use an external time-stamped registration or preregistration system before looking at outcomes. The repository record is a reproducibility aid, not proof of preregistration.

## Validation

A credible empirical study should:

- verify assignment implementation
- report baseline summaries without treating balance tests as proof of successful randomization
- pre-specify the primary outcome and analysis
- report attrition by group
- document noncompliance and contamination
- justify missing-data handling
- report uncertainty
- distinguish exploratory from confirmatory analyses
- retain a clear audit trail for protocol changes

## Threats to validity

Small samples, attrition, noncompliance, treatment contamination, outcome switching, multiple testing, measurement changes, ceiling/floor effects, interference between participants, cluster structure, and selective reporting can all undermine interpretation.

A randomized assignment procedure alone does not guarantee that every analysis supports a causal claim.
