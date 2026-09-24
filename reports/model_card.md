# Analytic system card

## System

Learning Experiment Platform

## Purpose

A transparent research scaffold for small two-group learning experiments with reproducible assignment, pre/post outcomes, effect estimates, bootstrap uncertainty, and attrition review.

## Current maturity

Working research prototype. The bundled example is synthetic and demonstrates the software path only. It does not establish an educational treatment effect.

## Inputs

The integrated analysis expects participant records containing:

- participant ID
- assigned group
- finite numeric pre score
- finite numeric post score or a missing post value

## Outputs

The current analysis returns:

- participant and group counts
- observed outcome counts
- attrition counts and rates
- pre, post, and gain means by assigned group
- raw treatment-minus-control differences
- pooled-SD Cohen d when estimable
- seeded percentile-bootstrap confidence intervals for raw mean differences
- transparent analysis flags
- assignment and analysis method labels

## Assignment and analysis distinction

The software can create a seeded random assignment, but `analyze_experiment()` does not assume that every dataset was randomized. The caller records the assignment method explicitly.

The current outcome analysis stays grouped by assigned group. Missing post outcomes are counted as attrition and omitted from complete-case post/gain estimates.

## Not-estimable states

Cohen d is not forced to zero when the pooled standard deviation is zero. It is returned as not estimable.

Effects are also left unestimated when too few observed outcomes remain in a group.

## Evidence needed before real use

A real study should document recruitment, assignment, intervention fidelity, primary outcome, sample size rationale, exclusions, missing-data strategy, attrition, noncompliance, contamination, protocol deviations, and uncertainty.

## Main limitations

The current baseline:

- handles only two assigned groups
- uses complete cases for missing post outcomes
- does not implement cluster randomization
- does not implement covariate-adjusted models
- does not implement causal estimators for noncompliance
- does not implement quasi-experimental identification strategies
- does not provide p-values or model-based hypothesis tests
- does not prove that a study was preregistered

## Human oversight

Researchers must decide whether the design, measurements, missing-data assumptions, and causal interpretation are defensible. The software output should never substitute for that judgment.
