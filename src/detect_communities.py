
from pathlib import Path

import networkx as nx
import pandas as pd


# --------------------------------------------------
# 1. Locate project files
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RESULTS_DIR = PROJECT_ROOT / "results"

graph_path = RESULTS_DIR / "interaction_network.graphml"


# --------------------------------------------------
# 2. Load the original directed network
# --------------------------------------------------

directed_graph = nx.read_graphml(graph_path)

print("Original directed network loaded")
print(f"Users: {directed_graph.number_of_nodes()}")
print(f"Directed edges: {directed_graph.number_of_edges()}")


# --------------------------------------------------
# 3. Create an undirected weighted projection
# --------------------------------------------------

G = nx.Graph()

G.add_nodes_from(directed_graph.nodes())

for source, target, data in directed_graph.edges(data=True):

    weight = float(data.get("weight", 1))

    if G.has_edge(source, target):

        G[source][target]["weight"] += weight

    else:

        G.add_edge(
            source,
            target,
            weight=weight
        )

print("\nUndirected weighted network created")
print(f"Users: {G.number_of_nodes()}")
print(f"Undirected edges: {G.number_of_edges()}")


# --------------------------------------------------
# 4. Detect communities using Louvain
# --------------------------------------------------

communities = nx.community.louvain_communities(
    G,
    weight="weight",
    seed=42
)

modularity = nx.community.modularity(
    G,
    communities,
    weight="weight"
)


# --------------------------------------------------
# 5. Assign community IDs to users
# --------------------------------------------------

community_assignments = []

for community_id, members in enumerate(communities):

    for user_id in members:

        community_assignments.append({
            "user_id": user_id,
            "community_id": community_id
        })

assignments_df = pd.DataFrame(community_assignments)

assignments_df = assignments_df.sort_values(
    by=["community_id", "user_id"]
)


# --------------------------------------------------
# 6. Generate a community summary
# --------------------------------------------------

community_summary = []

for community_id, members in enumerate(communities):

    subgraph = G.subgraph(members)

    internal_weight = sum(
        data["weight"]
        for _, _, data in subgraph.edges(data=True)
    )

    community_summary.append({
        "community_id": community_id,
        "number_of_users": len(members),
        "internal_edges": subgraph.number_of_edges(),
        "internal_interaction_weight": internal_weight
    })

summary_df = pd.DataFrame(community_summary)

summary_df = summary_df.sort_values(
    by="number_of_users",
    ascending=False
)


# --------------------------------------------------
# 7. Save results
# --------------------------------------------------

assignments_df.to_csv(
    RESULTS_DIR / "community_assignments.csv",
    index=False
)

summary_df.to_csv(
    RESULTS_DIR / "community_summary.csv",
    index=False
)


# --------------------------------------------------
# 8. Display results
# --------------------------------------------------

print("\nLOUVAIN COMMUNITY DETECTION")
print("---------------------------")

print(f"Number of communities: {len(communities)}")
print(f"Modularity: {modularity:.4f}")

print("\nCommunity sizes:")

print(
    summary_df[
        ["community_id", "number_of_users", "internal_edges"]
    ].to_string(index=False)
)

print("\nLargest community:")
print(f"{summary_df.iloc[0]['number_of_users']} users")

print("\nFiles saved:")
print(RESULTS_DIR / "community_assignments.csv")
print(RESULTS_DIR / "community_summary.csv")

print("\nReminder: These results use synthetic data.")
