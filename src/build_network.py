
"""
Build a directed user interaction network from synthetic Reddit data.

A directed edge A -> B means user A replied to user B.

All data in this project stage is synthetic.
"""

from pathlib import Path

import pandas as pd
import networkx as nx


# --------------------------------------------------
# 1. LOAD DATA
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data" / "mock"
RESULTS_DIR = PROJECT_ROOT / "results"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)

posts = pd.read_csv(DATA_DIR / "posts.csv")
comments = pd.read_csv(DATA_DIR / "comments.csv")


# --------------------------------------------------
# 2. CREATE LOOKUP TABLES
# --------------------------------------------------

# Map every post ID to its author.
post_authors = (
    posts.set_index("id")["author_hash"].to_dict()
)

# Map every comment ID to its author.
comment_authors = (
    comments.set_index("id")["author_hash"].to_dict()
)


# --------------------------------------------------
# 3. INITIALISE DIRECTED GRAPH
# --------------------------------------------------

G = nx.DiGraph()

# Add users who authored posts.
for author in posts["author_hash"].unique():
    G.add_node(author)

# Add users who authored comments.
for author in comments["author_hash"].unique():
    G.add_node(author)


# --------------------------------------------------
# 4. CREATE INTERACTION EDGES
# --------------------------------------------------

self_replies = 0
interaction_count = 0

for _, comment in comments.iterrows():

    replying_user = comment["author_hash"]
    parent_id = comment["parent_id"]
    post_id = comment["post_id"]

    # Identify the author receiving the reply.
    if parent_id == post_id:

        receiving_user = post_authors[post_id]

    else:

        receiving_user = comment_authors[parent_id]

    # Exclude replies to oneself from user-user interactions.
    if replying_user == receiving_user:
        self_replies += 1
        continue

    # Add or update the directed edge.
    if G.has_edge(replying_user, receiving_user):

        G[replying_user][receiving_user]["weight"] += 1

    else:

        G.add_edge(
            replying_user,
            receiving_user,
            weight=1
        )

    interaction_count += 1


# --------------------------------------------------
# 5. CALCULATE NODE-LEVEL METRICS
# --------------------------------------------------

node_rows = []

for node in G.nodes():

    node_rows.append({
        "user_id": node,

        # Number of distinct users this person replied to.
        "out_degree": G.out_degree(node),

        # Number of distinct users who replied to this person.
        "in_degree": G.in_degree(node),

        # Total outgoing reply interactions.
        "out_strength": G.out_degree(node, weight="weight"),

        # Total incoming reply interactions.
        "in_strength": G.in_degree(node, weight="weight"),

        "degree_centrality": nx.degree_centrality(G),

        "in_degree_centrality": nx.in_degree_centrality(G)[node],

        "out_degree_centrality": nx.out_degree_centrality(G)[node],
    })


nodes_df = pd.DataFrame(node_rows)

# The dictionary returned by degree_centrality is the same for
# every row. Replace that column with its corresponding node value.
degree_centralities = nx.degree_centrality(G)

nodes_df["degree_centrality"] = (
    nodes_df["user_id"].map(degree_centralities)
)


# --------------------------------------------------
# 6. CALCULATE NETWORK-LEVEL METRICS
# --------------------------------------------------

number_of_nodes = G.number_of_nodes()
number_of_edges = G.number_of_edges()

density = nx.density(G)

reciprocity = nx.reciprocity(G)

weak_components = list(nx.weakly_connected_components(G))
strong_components = list(nx.strongly_connected_components(G))

largest_weak_component = max(
    (len(component) for component in weak_components),
    default=0
)

largest_strong_component = max(
    (len(component) for component in strong_components),
    default=0
)

pagerank = nx.pagerank(G, weight="weight")

nodes_df["pagerank"] = nodes_df["user_id"].map(pagerank)


# --------------------------------------------------
# 7. EXPORT EDGE LIST
# --------------------------------------------------

edge_rows = []

for source, target, attributes in G.edges(data=True):

    edge_rows.append({
        "source_user": source,
        "target_user": target,
        "interaction_count": attributes["weight"],
    })

edges_df = pd.DataFrame(
    edge_rows,
    columns=[
        "source_user",
        "target_user",
        "interaction_count"
    ]
)


# --------------------------------------------------
# 8. SAVE OUTPUTS
# --------------------------------------------------

nodes_df.to_csv(
    RESULTS_DIR / "network_nodes.csv",
    index=False
)

edges_df.to_csv(
    RESULTS_DIR / "network_edges.csv",
    index=False
)

nx.write_graphml(
    G,
    RESULTS_DIR / "interaction_network.graphml"
)


# --------------------------------------------------
# 9. DISPLAY RESULTS
# --------------------------------------------------

print("\nUSER INTERACTION NETWORK")
print("------------------------")

print(f"Number of users: {number_of_nodes}")
print(f"Distinct directed edges: {number_of_edges}")
print(f"Total reply interactions: {interaction_count}")
print(f"Self-replies excluded: {self_replies}")

print(f"\nNetwork density: {density:.4f}")

if reciprocity is not None:
    print(f"Network reciprocity: {reciprocity:.4f}")
else:
    print("Network reciprocity: Not defined")

print(f"Weakly connected components: {len(weak_components)}")
print(f"Strongly connected components: {len(strong_components)}")

print(
    f"Largest weak component: "
    f"{largest_weak_component} users"
)

print(
    f"Largest strong component: "
    f"{largest_strong_component} users"
)

print("\nTop 10 users by PageRank:")

print(
    nodes_df.sort_values(
        "pagerank",
        ascending=False
    )[
        ["user_id", "pagerank", "in_degree", "out_degree"]
    ].head(10).to_string(index=False)
)

print("\nFiles saved:")
print(RESULTS_DIR / "network_nodes.csv")
print(RESULTS_DIR / "network_edges.csv")
print(RESULTS_DIR / "interaction_network.graphml")

print("\nREMINDER: This network is based entirely on synthetic data.")
