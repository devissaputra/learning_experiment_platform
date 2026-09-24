# Data Documentation

## Included data

`sample.csv` contains a synthetic pre/post learning experiment with 12 participant IDs. Six are assigned to treatment and six to control. One control post-test value is intentionally missing so the attrition path can be demonstrated.

No row represents a real learner.

## Current schema

- `participant_id`: unique synthetic participant identifier
- `assigned_group`: `treatment` or `control`
- `pre`: baseline outcome measured before the intervention
- `post`: primary post-intervention outcome; blank means the outcome was not observed

The integrated analysis groups participants by **assigned group**.

## Current missing-outcome rule

A missing post value is counted as attrition. The current effect analysis is complete-case by assigned group:

- the participant remains in assignment and attrition counts
- no post-test value is imputed
- the participant is excluded from post and gain means/effect calculations

This is a transparent baseline, not a complete missing-data strategy.

## Assignment provenance

For a randomized experiment, store the assignment seed or the external assignment procedure alongside the dataset. The bundled demo uses a seeded two-group random assignment.

Do not reconstruct assignment from post-treatment information.

## Minimum experiment metadata

For a real study, record at least:

- experiment ID and version
- hypothesis
- primary outcome
- assignment procedure
- assignment seed where applicable
- intervention and control conditions
- recruitment and eligibility rules
- exclusion rules
- planned sample size
- analysis plan
- outcome timing
- protocol deviations
- attrition reasons when known

A code-generated metadata record is useful for reproducibility, but it is not the same as a time-stamped preregistration.

## Validation rules

Before analysis, verify:

- unique participant IDs
- valid assigned-group labels
- finite numeric baseline values
- whether missing post outcomes are expected and correctly encoded
- whether the observed data correspond to the planned primary outcome
- whether treatment contamination or noncompliance occurred

## Do not commit

Do not commit identifiable learner records, protected educational records, consent forms containing personal information, private LMS exports, or datasets whose license or ethics approval prohibits redistribution.

## Dataset card requirement

For empirical work, document the population, recruitment, consent or lawful basis, intervention, comparison condition, outcome measures, assignment mechanism, collection dates, exclusions, missingness, attrition, protocol deviations, known biases, security requirements, and permitted uses.
