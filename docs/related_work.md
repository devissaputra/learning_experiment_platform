# Related work and methodological context

Learning Experiment Platform is an original, compact implementation for transparent two-group learning experiments. It is not intended to replace mature statistical or trial-management software.

## Standardized mean differences

The current `cohens_d()` function uses the difference between treatment and control means divided by the pooled standard deviation.

A public reference implementation and formula are available from the U.S. National Institute of Standards and Technology:

- NIST Dataplot, effect-size statistics: https://www.itl.nist.gov/div898/software/dataplot/refman2/auxillar/hedgeg.htm

For small samples, researchers may prefer bias-corrected Hedges g. That correction is not implemented in the current baseline.

## Bootstrap uncertainty

The repository uses a seeded percentile bootstrap for confidence intervals around **raw mean differences**. This keeps the implementation inspectable and dependency-free.

The current baseline does not claim that percentile bootstrap intervals are optimal for every design. Clustered data, repeated measures, very small samples, or complex assignment structures may require different methods.

## Preregistration and transparent research records

The Open Science Framework supports registrations and preregistrations that can preserve a time-stamped study plan:

- OSF registrations and preregistrations: https://help.osf.io/article/330-welcome-to-registrations
- OSF overview: https://help.osf.io/article/342-getting-started-on-the-osf

The repository's `experiment_record()` function is intentionally described as local metadata, not as proof of preregistration.

## Randomized-trial reporting

For formal randomized trials, researchers should use reporting guidance appropriate to the design and field rather than treating this repository's output as a complete trial report.

The CONSORT initiative provides reporting guidance for randomized trials:

- https://www.consort-statement.org/

## Relationship to this repository

The goal here is narrower:

1. keep assignment reproducible
2. keep pre/post transformations visible
3. report raw and standardized effects separately
4. surface attrition instead of hiding it
5. make uncertainty reproducible
6. preserve enough analysis metadata to audit what was done

Future work should benchmark the implementation against established statistical libraries and reproduce a public learning experiment from raw data to reported estimates.
