import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from learning_experiment_platform.core import (
    analyze_experiment,
    assign,
    experiment_record,
)


participant_ids = [f"P{index:02d}" for index in range(1, 13)]
assignment_seed = 42
assignment = assign(participant_ids, seed=assignment_seed)

pre_scores = {
    "P01": 61,
    "P02": 65,
    "P03": 58,
    "P04": 59,
    "P05": 67,
    "P06": 66,
    "P07": 68,
    "P08": 62,
    "P09": 70,
    "P10": 64,
    "P11": 69,
    "P12": 63,
}

post_scores = {
    "P01": 68,
    "P02": 71,
    "P03": 68,
    "P04": 65,
    "P05": 73,
    "P06": 76,
    "P07": 77,
    "P08": 73,
    "P09": 80,
    "P10": 74,
    "P11": None,
    "P12": 70,
}

records = [
    {
        "participant_id": participant_id,
        "assigned_group": assignment[participant_id],
        "pre": pre_scores[participant_id],
        "post": post_scores[participant_id],
    }
    for participant_id in participant_ids
]

spec = experiment_record(
    "DEMO-001",
    "The synthetic learning-design intervention increases post-test performance.",
    "post-test score",
    assignment_seed=assignment_seed,
    exclusion_rule="No post-test value is imputed; missing post outcomes remain attrition.",
)

result = analyze_experiment(
    records,
    assignment_method="seeded_random_assignment",
)

print("Experiment:", spec["experiment_id"])
print("Assignment seed:", spec["assignment_seed"])
print("Assigned:", result["assigned_counts"])
print("Observed:", result["observed_counts"])
print(f"Overall attrition: {result['overall_attrition_rate']:.3f}")
print("Pre means:", result["pre_means"])
print("Post means:", result["post_means"])
print("Gain means:", result["gain_means"])
print(f"Post mean difference: {result['post_mean_difference']:.3f}")
print(f"Gain mean difference: {result['gain_mean_difference']:.3f}")
print(
    "Post Cohen d:",
    (
        f"{result['post_cohens_d']:.3f}"
        if result["post_cohens_d"] is not None
        else "not estimable"
    ),
)
print(
    "Gain Cohen d:",
    (
        f"{result['gain_cohens_d']:.3f}"
        if result["gain_cohens_d"] is not None
        else "not estimable"
    ),
)
print("Post mean-difference CI:", result["post_mean_difference_ci"])
print("Gain mean-difference CI:", result["gain_mean_difference_ci"])
print("Analysis flags:", result["analysis_flags"] or ["none"])
print("Note: this is a synthetic software demonstration, not an empirical finding.")
