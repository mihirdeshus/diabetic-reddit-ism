
def calculate_test_virality(parent_map, root_id="post"):
    """
    Calculate average pairwise distance in a rooted tree.

    parent_map maps each comment ID to its parent ID.
    """

    n = len(parent_map) + 1

    subtree_size = {root_id: 1}

    for comment_id in parent_map:
        subtree_size[comment_id] = 1

    # Calculate the depth of every node.
    depths = {root_id: 0}

    for comment_id, parent_id in parent_map.items():
        current = comment_id
        depth = 0

        while current != root_id:
            current = parent_map[current]
            depth += 1

        depths[comment_id] = depth

    # Process deepest nodes first.
    ordered_nodes = sorted(
        parent_map,
        key=lambda node: depths[node],
        reverse=True
    )

    total_distance = 0

    for node in ordered_nodes:

        parent = parent_map[node]
        size = subtree_size[node]

        total_distance += size * (n - size)

        subtree_size[parent] += size

    pairs = n * (n - 1) / 2

    return total_distance / pairs


# Test 1: Four comments directly reply to the post.
star = {
    "c1": "post",
    "c2": "post",
    "c3": "post",
    "c4": "post"
}

# Test 2: Each comment replies to the previous comment.
chain = {
    "c1": "post",
    "c2": "c1",
    "c3": "c2",
    "c4": "c3"
}


star_result = calculate_test_virality(star)
chain_result = calculate_test_virality(chain)

print("STRUCTURAL VIRALITY UNIT TESTS")
print("------------------------------")

print(f"Star-shaped tree: {star_result:.4f}")
print(f"Chain-shaped tree: {chain_result:.4f}")

assert abs(star_result - 1.6) < 1e-9
assert abs(chain_result - 2.0) < 1e-9
assert chain_result > star_result

print("\nAll structural virality tests passed!")
