
from pathlib import Path

import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


# --------------------------------------------------
# 1. Locate and load files
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RESULTS_DIR = PROJECT_ROOT / "results"
FIGURES_DIR = PROJECT_ROOT / "figures"

FIGURES_DIR.mkdir(exist_ok=True)

directed_graph = nx.read_graphml(
    RESULTS_DIR / "interaction_network.graphml"
)

assignments = pd.read_csv(
    RESULTS_DIR / "community_assignments.csv"
)


# --------------------------------------------------
# 2. Recreate the undirected weighted network
# --------------------------------------------------

G = nx.Graph()

G.add_nodes_from(directed_graph.nodes())

for source, target, data in directed_graph.edges(data=True):

    weight = float(data.get("weight", 1))

    if G.has_edge(source, target):
        G[source][target]["weight"] += weight
    else:
        G.add_edge(source, target, weight=weight)


# --------------------------------------------------
# 3. Create user-to-community mapping
# --------------------------------------------------

community_map = dict(
    zip(
        assignments["user_id"].astype(str),
        assignments["community_id"]
    )
)

communities = sorted(assignments["community_id"].unique())

# Check that every graph node has an assignment.
assert set(G.nodes()) == set(community_map.keys()), (
    "Graph nodes and community assignments do not match!"
)


# --------------------------------------------------
# 4. Calculate node sizes using PageRank
# --------------------------------------------------

pagerank = nx.pagerank(G, weight="weight")

node_sizes = [
    300 + pagerank[node] * 50000
    for node in G.nodes()
]


# --------------------------------------------------
# 5. Calculate positions
# --------------------------------------------------

pos = nx.spring_layout(
    G,
    seed=42,
    k=0.25,
    iterations=150,
    weight="weight"
)


# --------------------------------------------------
# 6. Draw the network
# --------------------------------------------------

plt.figure(figsize=(16, 12))

nx.draw_networkx_edges(
    G,
    pos,
    alpha=0.12,
    width=0.5,
    edge_color="gray"
)

cmap = plt.get_cmap("tab10")

for community_id in communities:

    members = [
        node for node in G.nodes()
        if community_map[node] == community_id
    ]

    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=members,
        node_size=[
            node_sizes[list(G.nodes()).index(node)]
            for node in members
        ],
        node_color=[cmap(int(community_id) % 10)],
        label=f"Community {community_id}",
        alpha=0.9
    )


# --------------------------------------------------
# 7. Add legend and title
# --------------------------------------------------

legend_items = [
    Patch(
        facecolor=cmap(int(cid) % 10),
        label=f"Community {cid}"
    )
    for cid in communities
]

plt.legend(
    handles=legend_items,
    title="Detected communities",
    loc="upper left",
    bbox_to_anchor=(1, 1)
)

plt.title(
    "Louvain Communities in the Synthetic User Interaction Network",
    fontsize=15
)

plt.axis("off")
plt.tight_layout()


# --------------------------------------------------
# 8. Save figure
# --------------------------------------------------

output_path = FIGURES_DIR / "community_network.png"

plt.savefig(
    output_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Community visualisation created successfully.")
print(output_path)
print("\nReminder: This figure uses synthetic data.")
