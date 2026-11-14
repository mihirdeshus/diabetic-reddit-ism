
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


# --------------------------------------------------
# 1. Locate and load the data
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RESULTS_DIR = PROJECT_ROOT / "results"

data = pd.read_csv(
    RESULTS_DIR / "structural_virality.csv"
)

# Keep only rows with valid measurements.
data = data.dropna(
    subset=[
        "structural_virality",
        "num_comments",
        "theme",
        "subreddit"
    ]
).copy()

data["num_comments"] = pd.to_numeric(
    data["num_comments"],
    errors="raise"
)

data["structural_virality"] = pd.to_numeric(
    data["structural_virality"],
    errors="raise"
)


# --------------------------------------------------
# 2. Descriptive statistics by theme
# --------------------------------------------------

theme_summary = (
    data.groupby("theme")["structural_virality"]
    .agg(
        post_count="count",
        mean="mean",
        median="median",
        std="std"
    )
    .sort_values("mean", ascending=False)
)

print("\nSTRUCTURAL VIRALITY BY THEME")
print("----------------------------")

print(theme_summary.round(4).to_string())


# --------------------------------------------------
# 3. Fit an adjusted regression model
# --------------------------------------------------

# log1p transforms comment count to reduce
# the influence of differences between small
# and large discussions.

data["log_comments"] = np.log1p(
    data["num_comments"]
)

model = smf.ols(
    formula=(
        "structural_virality ~ "
        "C(theme) + log_comments + C(subreddit)"
    ),
    data=data
).fit(cov_type="HC3")


# --------------------------------------------------
# 4. Display the regression results
# --------------------------------------------------

print("\nADJUSTED REGRESSION RESULTS")
print("---------------------------")

print(model.summary())


# --------------------------------------------------
# 5. Joint test of theme effects
# --------------------------------------------------

theme_terms = [
    term for term in model.params.index
    if term.startswith("C(theme)")
]

hypothesis = " = 0, ".join(theme_terms) + " = 0"

theme_test = model.f_test(hypothesis)

print("\nJOINT TEST OF THEME EFFECTS")
print("---------------------------")

print(f"F-statistic: {float(theme_test.fvalue):.4f}")
print(f"P-value: {float(theme_test.pvalue):.4f}")


# --------------------------------------------------
# 6. Save the results
# --------------------------------------------------

theme_summary.to_csv(
    RESULTS_DIR / "theme_virality_summary.csv"
)

coefficients = pd.DataFrame({
    "coefficient": model.params,
    "standard_error": model.bse,
    "p_value": model.pvalues
})

coefficients.to_csv(
    RESULTS_DIR / "theme_virality_regression.csv"
)

print("\nFiles saved:")
print(RESULTS_DIR / "theme_virality_summary.csv")
print(RESULTS_DIR / "theme_virality_regression.csv")

print("\nReminder: These results use synthetic data.")
