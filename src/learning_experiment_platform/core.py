import math
import random


def assign(ids, seed=42):
    """Randomly assign roughly half of unique participant IDs to treatment."""
    ids = list(ids)
    if len(ids) < 2:
        raise ValueError("at least two participant IDs are required")
    if len(set(ids)) != len(ids):
        raise ValueError("participant IDs must be unique")
    rng = random.Random(seed)
    shuffled = ids[:]
    rng.shuffle(shuffled)
    split = len(shuffled) // 2
    return {
        participant: ("treatment" if index < split else "control")
        for index, participant in enumerate(shuffled)
    }


def mean(values):
    values = list(values)
    if not values:
        raise ValueError("values must not be empty")
    return sum(values) / len(values)


def cohens_d(treatment, control):
    """Return pooled standard deviation Cohen d for two independent groups."""
    treatment = list(treatment)
    control = list(control)
    if len(treatment) < 2 or len(control) < 2:
        raise ValueError("each group must contain at least two observations")
    mean_treatment = mean(treatment)
    mean_control = mean(control)
    var_treatment = sum((x - mean_treatment) ** 2 for x in treatment) / (len(treatment) - 1)
    var_control = sum((x - mean_control) ** 2 for x in control) / (len(control) - 1)
    pooled = math.sqrt(
        ((len(treatment) - 1) * var_treatment + (len(control) - 1) * var_control)
        / (len(treatment) + len(control) - 2)
    )
    return 0.0 if pooled == 0 else (mean_treatment - mean_control) / pooled


def gain(post, pre):
    """Return paired post minus pre change scores."""
    post = list(post)
    pre = list(pre)
    if len(post) != len(pre) or not post:
        raise ValueError("post and pre must be non-empty and have equal length")
    return [after - before for before, after in zip(pre, post)]
