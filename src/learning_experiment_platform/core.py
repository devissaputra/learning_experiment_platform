# Calculation reading guide: ../CALCULATIONS.md (repository root).
# Cohen d = (mean treatment - mean control)/pooled sample SD.
# Complete-case analysis by assignment is not a full intention-to-treat estimate when outcomes are missing. Observational assignment and attrition can undermine causal claims even when a mean difference is precise.

import math
import random
from collections.abc import Mapping, Sequence
from numbers import Real


GROUPS = ("treatment", "control")


def _as_finite_numbers(values, name):
    values = list(values)
    if not values:
        raise ValueError(f"{name} must not be empty")
    for value in values:
        if isinstance(value, bool) or not isinstance(value, Real):
            raise ValueError(f"{name} must contain only numeric values")
        if not math.isfinite(float(value)):
            raise ValueError(f"{name} must contain only finite values")
    return values


def mean(values):
    values = _as_finite_numbers(values, "values")
    return sum(values) / len(values)


def assign(ids, seed=42):
    """Assign unique participant IDs to two groups with size difference <= 1."""
    ids = list(ids)
    if len(ids) < 2:
        raise ValueError("at least two participant IDs are required")
    try:
        unique_count = len(set(ids))
    except TypeError as exc:
        raise ValueError("participant IDs must be hashable") from exc
    if unique_count != len(ids):
        raise ValueError("participant IDs must be unique")

    rng = random.Random(seed)
    shuffled = ids[:]
    rng.shuffle(shuffled)
    split = len(shuffled) // 2

    return {
        participant: ("treatment" if index < split else "control")
        for index, participant in enumerate(shuffled)
    }


def gain(post, pre):
    """Return paired post-minus-pre change scores."""
    post = list(post)
    pre = list(pre)
    if len(post) != len(pre) or not post:
        raise ValueError("post and pre must be non-empty and have equal length")
    post = _as_finite_numbers(post, "post")
    pre = _as_finite_numbers(pre, "pre")
    return [after - before for before, after in zip(pre, post)]


def _sample_variance(values):
    values = _as_finite_numbers(values, "values")
    if len(values) < 2:
        raise ValueError("sample variance requires at least two observations")
    value_mean = mean(values)
    return sum((value - value_mean) ** 2 for value in values) / (len(values) - 1)


def cohens_d(treatment, control):
    """Return pooled-SD Cohen d for two independent groups.

    None means the standardized effect is not estimable because the pooled
    standard deviation is zero.
    """
    treatment = _as_finite_numbers(treatment, "treatment")
    control = _as_finite_numbers(control, "control")
    if len(treatment) < 2 or len(control) < 2:
        raise ValueError("each group must contain at least two observations")

    mean_treatment = mean(treatment)
    mean_control = mean(control)
    var_treatment = _sample_variance(treatment)
    var_control = _sample_variance(control)

    pooled_variance = (
        (len(treatment) - 1) * var_treatment
        + (len(control) - 1) * var_control
    ) / (len(treatment) + len(control) - 2)

    if math.isclose(pooled_variance, 0.0, abs_tol=1e-12):
        return None

    return (mean_treatment - mean_control) / math.sqrt(pooled_variance)


def _percentile(sorted_values, probability):
    if not 0 <= probability <= 1:
        raise ValueError("probability must be between 0 and 1")
    if len(sorted_values) == 1:
        return sorted_values[0]

    position = probability * (len(sorted_values) - 1)
    lower_index = int(math.floor(position))
    upper_index = int(math.ceil(position))
    if lower_index == upper_index:
        return sorted_values[lower_index]

    weight = position - lower_index
    return (
        sorted_values[lower_index] * (1 - weight)
        + sorted_values[upper_index] * weight
    )


def bootstrap_mean_difference_ci(
    treatment,
    control,
    *,
    confidence=0.95,
    iterations=2000,
    seed=42,
):
    """Percentile bootstrap CI for treatment-minus-control mean difference."""
    treatment = _as_finite_numbers(treatment, "treatment")
    control = _as_finite_numbers(control, "control")

    if len(treatment) < 2 or len(control) < 2:
        raise ValueError("each group must contain at least two observations")
    if not 0 < confidence < 1:
        raise ValueError("confidence must be between 0 and 1")
    if iterations < 100:
        raise ValueError("iterations must be at least 100")

    rng = random.Random(seed)
    differences = []

    for _ in range(iterations):
        sampled_treatment = [
            treatment[rng.randrange(len(treatment))]
            for _ in treatment
        ]
        sampled_control = [
            control[rng.randrange(len(control))]
            for _ in control
        ]
        differences.append(
            mean(sampled_treatment) - mean(sampled_control)
        )

    differences.sort()
    alpha = 1 - confidence
    return (
        _percentile(differences, alpha / 2),
        _percentile(differences, 1 - alpha / 2),
    )


def experiment_record(
    experiment_id,
    hypothesis,
    primary_outcome,
    *,
    assignment_seed=42,
    exclusion_rule="none specified",
    analysis_method="complete cases analyzed by assigned group",
):
    """Create a compact, serializable analysis record for a planned experiment."""
    fields = {
        "experiment_id": experiment_id,
        "hypothesis": hypothesis,
        "primary_outcome": primary_outcome,
        "exclusion_rule": exclusion_rule,
        "analysis_method": analysis_method,
    }
    for name, value in fields.items():
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must be a non-empty string")

    if isinstance(assignment_seed, bool) or not isinstance(assignment_seed, int):
        raise ValueError("assignment_seed must be an integer")

    return {
        **fields,
        "assignment_seed": assignment_seed,
    }


def _validate_records(records):
    records = list(records)
    if len(records) < 2:
        raise ValueError("at least two participant records are required")

    ids = []
    normalized = []

    for index, record in enumerate(records):
        if not isinstance(record, Mapping):
            raise ValueError(f"record {index} must be a mapping")

        missing = {
            key
            for key in ("participant_id", "assigned_group", "pre", "post")
            if key not in record
        }
        if missing:
            raise ValueError(
                f"record {index} is missing required fields: {sorted(missing)}"
            )

        participant_id = record["participant_id"]
        group = record["assigned_group"]
        pre = record["pre"]
        post = record["post"]

        try:
            hash(participant_id)
        except TypeError as exc:
            raise ValueError("participant IDs must be hashable") from exc

        if group not in GROUPS:
            raise ValueError(
                "assigned_group must be 'treatment' or 'control'"
            )

        _as_finite_numbers([pre], f"record {index} pre")
        if post is not None:
            _as_finite_numbers([post], f"record {index} post")

        ids.append(participant_id)
        normalized.append(
            {
                "participant_id": participant_id,
                "assigned_group": group,
                "pre": float(pre),
                "post": None if post is None else float(post),
            }
        )

    if len(set(ids)) != len(ids):
        raise ValueError("participant IDs must be unique")

    if {record["assigned_group"] for record in normalized} != set(GROUPS):
        raise ValueError("records must include treatment and control groups")

    return normalized


def _effect_or_none(treatment, control):
    if len(treatment) < 2 or len(control) < 2:
        return None
    return cohens_d(treatment, control)


def _ci_or_none(
    treatment,
    control,
    *,
    confidence,
    bootstrap_iterations,
    bootstrap_seed,
):
    if len(treatment) < 2 or len(control) < 2:
        return None
    return bootstrap_mean_difference_ci(
        treatment,
        control,
        confidence=confidence,
        iterations=bootstrap_iterations,
        seed=bootstrap_seed,
    )


def analyze_experiment(
    records,
    *,
    assignment_method="unknown",
    confidence=0.95,
    bootstrap_iterations=2000,
    bootstrap_seed=42,
    differential_attrition_threshold=0.10,
    baseline_smd_threshold=0.25,
):
    """Analyze pre/post outcomes by assigned group with transparent safeguards.

    Post=None is treated as an unobserved primary outcome for attrition
    summaries. The current analysis is complete-case and remains grouped by
    assignment, not by treatment received.
    """
    records = _validate_records(records)

    if not isinstance(assignment_method, str) or not assignment_method.strip():
        raise ValueError("assignment_method must be a non-empty string")
    if not 0 <= differential_attrition_threshold <= 1:
        raise ValueError(
            "differential_attrition_threshold must be between 0 and 1"
        )
    if baseline_smd_threshold < 0:
        raise ValueError("baseline_smd_threshold must be non-negative")

    assigned = {
        group: [record for record in records if record["assigned_group"] == group]
        for group in GROUPS
    }
    observed = {
        group: [record for record in assigned[group] if record["post"] is not None]
        for group in GROUPS
    }

    assigned_counts = {group: len(assigned[group]) for group in GROUPS}
    observed_counts = {group: len(observed[group]) for group in GROUPS}
    attrition_counts = {
        group: assigned_counts[group] - observed_counts[group]
        for group in GROUPS
    }
    attrition_rates = {
        group: attrition_counts[group] / assigned_counts[group]
        for group in GROUPS
    }

    pre = {
        group: [record["pre"] for record in assigned[group]]
        for group in GROUPS
    }
    post = {
        group: [record["post"] for record in observed[group]]
        for group in GROUPS
    }
    gains = {
        group: [
            record["post"] - record["pre"]
            for record in observed[group]
        ]
        for group in GROUPS
    }

    pre_means = {group: mean(pre[group]) for group in GROUPS}
    post_means = {
        group: mean(post[group]) if post[group] else None
        for group in GROUPS
    }
    gain_means = {
        group: mean(gains[group]) if gains[group] else None
        for group in GROUPS
    }

    baseline_difference = pre_means["treatment"] - pre_means["control"]
    post_difference = (
        None
        if None in post_means.values()
        else post_means["treatment"] - post_means["control"]
    )
    gain_difference = (
        None
        if None in gain_means.values()
        else gain_means["treatment"] - gain_means["control"]
    )

    baseline_d = _effect_or_none(pre["treatment"], pre["control"])
    post_d = _effect_or_none(post["treatment"], post["control"])
    gain_d = _effect_or_none(gains["treatment"], gains["control"])

    post_ci = _ci_or_none(
        post["treatment"],
        post["control"],
        confidence=confidence,
        bootstrap_iterations=bootstrap_iterations,
        bootstrap_seed=bootstrap_seed,
    )
    gain_ci = _ci_or_none(
        gains["treatment"],
        gains["control"],
        confidence=confidence,
        bootstrap_iterations=bootstrap_iterations,
        bootstrap_seed=bootstrap_seed + 1,
    )

    overall_attrition_count = sum(attrition_counts.values())
    overall_attrition_rate = overall_attrition_count / len(records)
    differential_attrition = (
        attrition_rates["treatment"] - attrition_rates["control"]
    )

    flags = []
    if overall_attrition_count:
        flags.append("attrition_present")
    if abs(differential_attrition) >= differential_attrition_threshold:
        flags.append("differential_attrition_review")
    if min(observed_counts.values()) < 2:
        flags.append("small_observed_group")
    if post_d is None:
        flags.append("post_effect_not_estimable")
    if gain_d is None:
        flags.append("gain_effect_not_estimable")
    if baseline_d is not None and abs(baseline_d) >= baseline_smd_threshold:
        flags.append("baseline_imbalance_review")

    return {
        "assignment_method": assignment_method,
        "analysis_method": "complete_case_by_assigned_group",
        "participant_count": len(records),
        "assigned_counts": assigned_counts,
        "observed_counts": observed_counts,
        "attrition_counts": attrition_counts,
        "attrition_rates": attrition_rates,
        "overall_attrition_rate": overall_attrition_rate,
        "differential_attrition_rate": differential_attrition,
        "pre_means": pre_means,
        "post_means": post_means,
        "gain_means": gain_means,
        "baseline_mean_difference": baseline_difference,
        "post_mean_difference": post_difference,
        "gain_mean_difference": gain_difference,
        "baseline_cohens_d": baseline_d,
        "post_cohens_d": post_d,
        "gain_cohens_d": gain_d,
        "confidence_level": confidence,
        "post_mean_difference_ci": post_ci,
        "gain_mean_difference_ci": gain_ci,
        "analysis_flags": flags,
    }
