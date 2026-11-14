
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


# --------------------------------------------------
# 1. Load data
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results"

data = pd.read_csv(
    RESULTS_DIR / "structural_virality.csv"
)

data = data.dropna(
    subset=[
        "structural_virality",
        "num_comments",
        "theme",
        "subreddit"
    ]
).copy()

data["log_comments"] = np.log1p(
    data["num_comments"]
)


# --------------------------------------------------
# 2. Original model
# --------------------------------------------------

formula_original = (
    "structural_virality ~ "
    "C(theme) + log_comments + C(subreddit)"
)

original_model = smf.ols(
    formula_original,
    data=data
).fit(cov_type="HC3")


# --------------------------------------------------
# 3. Identify influential observations
# --------------------------------------------------

# Refit without robust covariance to obtain
# the standard OLS influence diagnostics.

influence_model = smf.ols(
    formula_original,
    data=data
).fit()

cooks_distance = (
    influence_model.get_influence().cooks_distance[0]
)

threshold = 4 / len(data)

data["cooks_distance"] = cooks_distance

filtered_data = data[
    data["cooks_distance"] <= threshold
].copy()


# --------------------------------------------------
# 4. Model excluding flagged observations
# --------------------------------------------------

filtered_model = smf.ols(
    formula_original,
    data=filtered_data
).fit(cov_type="HC3")


# --------------------------------------------------
# 5. Model with categorical comment count
# --------------------------------------------------

categorical_model = smf.ols(
    "structural_virality ~ "
    "C(theme) + C(num_comments) + C(subreddit)",
    data=data
).fit(cov_type="HC3")


# --------------------------------------------------
# 6. Joint theme tests
# --------------------------------------------------

def get_theme_test(model):

    theme_terms = [
        term for term in model.params.index
        if term.startswith("C(theme)")
    ]

    hypothesis = " = 0, ".join(theme_terms) + " = 0"

    result = model.f_test(hypothesis)

    return float(result.fvalue), float(result.pvalue)


models = {
    "Original OLS": original_model,
    "Excluding Cook's flagged observations": filtered_model,
    "Categorical comment count": categorical_model
}


# --------------------------------------------------
# 7. Compare model results
# --------------------------------------------------

comparison = []

for name, model in models.items():

    f_stat, p_value = get_theme_test(model)

    comparison.append({
        "model": name,
        "observations": int(model.nobs),
        "r_squared": model.rsquared,
        "theme_F_statistic": f_stat,
        "theme_p_value": p_value
    })

comparison_df = pd.DataFrame(comparison)

print("\nSENSITIVITY ANALYSIS")
print("--------------------")

print(
    comparison_df.round(4).to_string(index=False)
)


# --------------------------------------------------
# 8. Save results
# --------------------------------------------------

comparison_df.to_csv(
    RESULTS_DIR / "sensitivity_analysis.csv",
    index=False
)

print("\nObservations flagged by Cook's distance:")
print(len(data) - len(filtered_data))

print("\nResults saved:")
print(RESULTS_DIR / "sensitivity_analysis.csv")

print("\nReminder: These results use synthetic data.")
