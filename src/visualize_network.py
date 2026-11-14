
from pathlib import Path

import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt


# --------------------------------------------------
# 1. Locate project files
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RESULTS_DIR = PROJECT_ROOT / "results"
FIGURES_DIR = PROJECT_ROOT / "figures"

FIGURES_DIR.mkdir(exist_ok=True)


# --------------------------------------------------
# 2. Load the interaction network
# --------------------------------------------------

graph_path = RESULTS_DIR / "interaction_network.graphml"

G = nx.read_graphml(graph_path)

nodes = pd.read_csv(RESULTS_DIR / "network_nodes.csv")

print("Network loaded successfully")
print(f"Users: {G.number_of_nodes()}")
print(f"Edges: {G.number_of_edges()}")


# --------------------------------------------------
# 3. Prepare node sizes using PageRank
# --------------------------------------------------

pagerank = nx.pagerank(G, weight="weight")

node_sizes = [
    1000 + pagerank[node] * 100000
    for node in G.nodes()
]

node_colors = [
    pagerank[node]
    for node in G.nodes()
]


# --------------------------------------------------
# 4. Draw the interaction network
# --------------------------------------------------

plt.figure(figsize=(16, 12))

pos = nx.spring_layout(
    G,
    seed=42,
    k=0.25,
    iterations=100,
    weight="weight"
)

nx.draw_networkx_edges(
    G,
    pos,
    alpha=0.12,
    width=0.5,
    edge_color="gray",
    arrows=False
)

nx.draw_networkx_nodes(
    G,
    pos,
    node_size=node_sizes,
    node_color=node_colors,
    cmap=plt.cm.viridis,
    alpha=0.9
)

plt.title(
    "Synthetic Diabetic Reddit User Interaction Network",
    fontsize=16
)

plt.axis("off")

plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "interaction_network.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# --------------------------------------------------
# 5. Plot PageRank distribution
# --------------------------------------------------

pagerank_values = list(pagerank.values())

plt.figure(figsize=(10, 6))

plt.hist(
    pagerank_values,
    bins=20,
    edgecolor="black"
)

plt.xlabel("PageRank")
plt.ylabel("Number of users")

plt.title("Distribution of PageRank Across Users")

plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "pagerank_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# --------------------------------------------------
# 6. Confirm saved figures
# --------------------------------------------------

print("\nVISUALISATIONS CREATED")
print("----------------------")

print(FIGURES_DIR / "interaction_network.png")
print(FIGURES_DIR / "pagerank_distribution.png")

print("\nReminder: These visualisations use synthetic data.")
