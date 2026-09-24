# Analytic system card

## System

Learning Experiment Platform

## Purpose

Small reproducible experiment scaffold for random assignment, pre and post gains, and Cohen d effect size.

## Current maturity

Working research prototype. The bundled example checks the software path with synthetic inputs. It does not establish validity for real learners, instructors, courses, or workplaces.

## Inputs

See `../data/README.md` for the current synthetic schema and the documentation expected before real data are connected.

## Outputs

The current code produces randomized group assignments, paired gain scores, and Cohen d effect size. These outputs are research signals and should be interpreted with the educational context that produced them.

## Evidence needed before real use

Verify randomization balance, pre specify outcomes, report uncertainty, and analyze attrition or missingness. Any causal conclusion must follow the actual assignment and compliance structure of the study.

## Main limitation

The code does not protect a study from bad randomization, selective outcome reporting, noncompliance, or weak measurement. It is an analysis scaffold, not an experiment management system.

## Human oversight

A person must review any output before it can affect a learner, instructor, applicant, or employee.
