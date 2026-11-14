
from pathlib import Path

import pandas as pd


# --------------------------------------------------
# 1. Locate files
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data" / "mock"
RESULTS_DIR = PROJECT_ROOT / "results"

RESULTS_DIR.mkdir(exist_ok=True)

posts = pd.read_csv(DATA_DIR / "posts.csv")
comments = pd.read_csv(DATA_DIR / "comments.csv")


# --------------------------------------------------
# 2. Calculate structural virality for one post
# --------------------------------------------------

def calculate_virality(post_id, post_comments):

    # One node for the original post,
    # plus one node for every comment.
    n = len(post_comments) + 1

    # No pairwise distance exists for one node.
    if n < 2:
        return None

    # Every node initially has subtree size 1.
    subtree_size = {post_id: 1}

    for comment in post_comments:
        subtree_size[comment["id"]] = 1

    # Process deeper comments before their parents.
    ordered_comments = sorted(
        post_comments,
        key=lambda c: c["depth"],
        reverse=True
    )

    total_distance = 0

    for comment in ordered_comments:

        comment_id = comment["id"]
        parent_id = comment["parent_id"]

        s = subtree_size[comment_id]

        # Removing this edge separates the tree
        # into groups of sizes s and n-s.
        # Every pair across those groups uses it.
        total_distance += s * (n - s)

        # Add this subtree to its parent.
        subtree_size[parent_id] += s

    # Number of unordered pairs of nodes.
    number_of_pairs = n * (n - 1) / 2

    return total_distance / number_of_pairs


# --------------------------------------------------
# 3. Group comments by post
# --------------------------------------------------

comments_by_post = {
    post_id: group.to_dict("records")
    for post_id, group in comments.groupby("post_id")
}


# --------------------------------------------------
# 4. Analyse every discussion tree
# --------------------------------------------------

results = []

for _, post in posts.iterrows():

    post_id = post["id"]

    post_comments = comments_by_post.get(
        post_id,
        []
    )

    virality = calculate_virality(
        post_id,
        post_comments
    )

    direct_replies = sum(
        comment["parent_id"] == post_id
        for comment in post_comments
    )

    max_depth = max(
        (comment["depth"] for comment in post_comments),
        default=0
    )

    result = {
        "post_id": post_id,
        "subreddit": post["subreddit"],
        "num_comments": len(post_comments),
        "tree_nodes": len(post_comments) + 1,
        "direct_replies": direct_replies,
        "max_depth": max_depth,
        "structural_virality": virality
    }

    # Include theme when present in the dataset.
    for column in ["theme", "primary_theme", "theme_id"]:
        if column in posts.columns:
            result["theme"] = post[column]
            break

    results.append(result)


# --------------------------------------------------
# 5. Save results
# --------------------------------------------------

results_df = pd.DataFrame(results)

output_path = RESULTS_DIR / "structural_virality.csv"

results_df.to_csv(
    output_path,
    index=False
)


# --------------------------------------------------
# 6. Display summary
# --------------------------------------------------

valid = results_df.dropna(
    subset=["structural_virality"]
)

print("\nSTRUCTURAL VIRALITY ANALYSIS")
print("---------------------------")

print(f"Posts analysed: {len(results_df)}")
print(f"Posts with measurable virality: {len(valid)}")

print(
    f"Mean structural virality: "
    f"{valid['structural_virality'].mean():.4f}"
)

print(
    f"Median structural virality: "
    f"{valid['structural_virality'].median():.4f}"
)

print(
    f"Maximum structural virality: "
    f"{valid['structural_virality'].max():.4f}"
)

print("\nTop 10 posts by structural virality:")

print(
    valid.sort_values(
        "structural_virality",
        ascending=False
    ).head(10).to_string(index=False)
)

print("\nResults saved:")
print(output_path)

print("\nReminder: These are synthetic discussions.")
