
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf


# --------------------------------------------------
# 1. Load data
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RESULTS_DIR = PROJECT_ROOT / "results"
FIGURES_DIR = PROJECT_ROOT / "figures"

FIGURES_DIR.mkdir(exist_ok=True)

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
# 2. Refit the model
# --------------------------------------------------

model = smf.ols(
    "structural_virality ~ C(theme) + log_comments + C(subreddit)",
    data=data
).fit(cov_type="HC3")

fitted = model.fittedvalues
residuals = model.resid


# --------------------------------------------------
# 3. Plot residuals against fitted values
# --------------------------------------------------

plt.figure(figsize=(9, 6))

plt.scatter(
    fitted,
    residuals,
    alpha=0.65
)

plt.axhline(
    0,
    linestyle="--"
)

plt.xlabel("Fitted values")
plt.ylabel("Residuals")

plt.title("Residuals vs Fitted Values")

plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "residuals_vs_fitted.png",
    dpi=300
)

plt.close()


# --------------------------------------------------
# 4. Plot actual vs predicted values
# --------------------------------------------------

plt.figure(figsize=(9, 6))

plt.scatter(
    fitted,
    data["structural_virality"],
    alpha=0.65
)

lower = min(
    fitted.min(),
    data["structural_virality"].min()
)

upper = max(
    fitted.max(),
    data["structural_virality"].max()
)

plt.plot(
    [lower, upper],
    [lower, upper],
    linestyle="--"
)

plt.xlabel("Predicted structural virality")
plt.ylabel("Actual structural virality")

plt.title("Actual vs Predicted Structural Virality")

plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "actual_vs_predicted.png",
    dpi=300
)

plt.close()


# --------------------------------------------------
# 5. Plot structural virality against comment count
# --------------------------------------------------

plt.figure(figsize=(9, 6))

plt.scatter(
    data["num_comments"],
    data["structural_virality"],
    alpha=0.65
)

plt.xlabel("Number of comments")
plt.ylabel("Structural virality")

plt.title("Structural Virality vs Discussion Size")

plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "virality_vs_comments.png",
    dpi=300
)

plt.close()


# --------------------------------------------------
# 6. Calculate influential observations
# --------------------------------------------------

influence = model.get_influence()

cooks_distance = influence.cooks_distance[0]

data["cooks_distance"] = cooks_distance

print("\nREGRESSION DIAGNOSTICS")
print("----------------------")

print(f"Observations: {len(data)}")
print(f"R-squared: {model.rsquared:.4f}")

print(
    "Observations with Cook's distance > 4/n:",
    int((data["cooks_distance"] > 4 / len(data)).sum())
)

print("\nLargest Cook's distances:")

print(
    data.nlargest(10, "cooks_distance")[
        ["num_comments", "structural_virality", "theme", "cooks_distance"]
    ].to_string(index=False)
)


# --------------------------------------------------
# 7. Save influence data
# --------------------------------------------------

data[
    ["num_comments", "structural_virality", "theme", "cooks_distance"]
].to_csv(
    RESULTS_DIR / "regression_influence.csv",
    index=False
)


print("\nDiagnostic figures saved:")
print(FIGURES_DIR / "residuals_vs_fitted.png")
print(FIGURES_DIR / "actual_vs_predicted.png")
print(FIGURES_DIR / "virality_vs_comments.png")

print("\nInfluence data saved:")
print(RESULTS_DIR / "regression_influence.csv")

print("\nReminder: These results use synthetic data.")
