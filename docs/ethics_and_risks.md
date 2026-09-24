# Ethics, safety, and misuse risks

## Intended use

Learning Experiment Platform is a research scaffold for designing and reviewing small learning experiments. It supports transparent analysis; it does not decide whether an intervention should be deployed or whether a causal claim is justified.

## Participant welfare

A learning experiment can impose real costs: time, frustration, reduced access to an effective activity, exposure to an ineffective activity, or unequal support.

Before a real study, researchers should consider:

- whether the comparison condition is ethically acceptable
- whether participants can withdraw without penalty where applicable
- whether the intervention creates avoidable academic disadvantage
- whether stopping or escalation rules are needed
- whether vulnerable participants require additional safeguards

## Consent and lawful basis

The software does not determine whether consent, institutional approval, parental permission, or another lawful basis is required.

Those decisions depend on jurisdiction, institution, participant population, intervention, data collected, and study purpose.

## Randomization ethics

Random assignment should not be treated as automatically ethical. The intervention and control conditions must both be defensible.

Do not randomize access to support that participants are already entitled to receive merely because the software can generate an assignment.

## Privacy

Pre/post learning outcomes can be sensitive educational records.

Use the minimum data required, separate direct identifiers from analysis data, restrict access to raw records, define retention periods, and avoid publishing small-cell information that can make participants identifiable.

## Attrition and exclusions

Selective exclusion can bias results. Record exclusions, missing outcomes, and attrition transparently.

Do not silently remove participants because their outcomes weaken the preferred conclusion.

## Analysis flexibility

Researchers can create misleading results by changing outcomes, subgroup definitions, exclusions, stopping rules, or analyses after seeing the data.

Use a pre-specified analysis plan for confirmatory work and clearly label exploratory analyses.

The local `experiment_record()` metadata is an audit aid. It is not a substitute for a time-stamped external preregistration.

## Causal claims

A randomized assignment can strengthen causal interpretation only when the design and implementation support it. Attrition, noncompliance, contamination, interference, measurement changes, and protocol deviations can weaken that interpretation.

Non-randomized datasets can be summarized with this code, but the current repository does not implement a quasi-experimental identification strategy.

## Uses excluded from this prototype

Do not use this software alone to:

- make high-stakes grading or admissions decisions
- withhold required educational support
- claim an intervention is proven effective
- conduct covert experimentation
- bypass research ethics or institutional review
- hide exclusions, missing outcomes, or protocol changes

## Before a real study

Document the study purpose, participant protections, consent or lawful basis, assignment procedure, primary outcome, analysis plan, data governance, intervention fidelity, stopping rules where relevant, attrition handling, adverse-event/escalation process where relevant, and how results will be communicated.
