
from pathlib import Path
import pandas as pd


# Locate project files
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "mock"

posts = pd.read_csv(DATA_DIR / "posts.csv")
comments = pd.read_csv(DATA_DIR / "comments.csv")


# 1. Check unique identifiers
assert posts["id"].is_unique, "Duplicate post IDs found!"
assert comments["id"].is_unique, "Duplicate comment IDs found!"

# 2. Check that every comment belongs to an existing post
post_ids = set(posts["id"])
comment_ids = set(comments["id"])

assert comments["post_id"].isin(post_ids).all(), (
    "Some comments refer to missing posts!"
)

# 3. Check parent relationships
comment_lookup = comments.set_index("id").to_dict("index")

for _, comment in comments.iterrows():

    parent_id = comment["parent_id"]
    post_id = comment["post_id"]

    if parent_id == post_id:
        assert comment["depth"] == 1, (
            f"Incorrect depth for {comment['id']}"
        )

    else:
        assert parent_id in comment_ids, (
            f"Missing parent comment: {parent_id}"
        )

        parent = comment_lookup[parent_id]

        assert parent["post_id"] == post_id, (
            f"Parent belongs to a different post: {comment['id']}"
        )

        assert comment["depth"] == parent["depth"] + 1, (
            f"Incorrect depth for {comment['id']}"
        )


# 4. Check comment counts against actual records
actual_counts = comments.groupby("post_id").size()

expected_counts = posts.set_index("id")["num_comments"]

assert (
    actual_counts.reindex(expected_counts.index, fill_value=0)
    == expected_counts
).all(), "Post comment counts do not match actual comment records!"


# 5. Check timestamps
posts["created_utc"] = pd.to_datetime(
    posts["created_utc"], utc=True, errors="raise"
)

comments["created_utc"] = pd.to_datetime(
    comments["created_utc"], utc=True, errors="raise"
)


# 6. Check chronological consistency
post_times = (
    posts.set_index("id")["created_utc"].to_dict()
)

comment_times = (
    comments.set_index("id")["created_utc"].to_dict()
)

for _, comment in comments.iterrows():

    parent_id = comment["parent_id"]

    if parent_id in post_times:
        parent_time = post_times[parent_id]
    else:
        parent_time = comment_times[parent_id]

    child_time = comment_times[comment["id"]]

    assert child_time > parent_time, (
        f"Comment {comment['id']} occurs before its parent!"
    )

    assert child_time <= pd.Timestamp.now(tz="UTC"), (
        f"Comment {comment['id']} occurs in the future!"
    )


# 7. Display validation results
print("\nDATA VALIDATION RESULTS")
print("-----------------------")

print("Unique post IDs: PASSED")
print("Unique comment IDs: PASSED")
print("Post references: PASSED")
print("Comment parent relationships: PASSED")
print("Comment depth consistency: PASSED")
print("Post comment counts: PASSED")
print("Timestamp formats: PASSED")
print("Chronological consistency: PASSED")

print("\nAll validation checks passed!")
print("Dataset is ready for network construction.")
print("Reminder: All records are synthetic.")
