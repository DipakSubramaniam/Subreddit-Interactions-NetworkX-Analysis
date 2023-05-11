import networkx as nx
import matplotlib.pyplot as plt
import math

TG = nx.read_gml('reddit_filtered.gml')

# Get the number of nodes and links in the original graph
num_nodes = TG.number_of_nodes()
num_links = TG.number_of_edges()

## Random

# Create multiple random graphs, p = 0.1 --> 0.5
random_graphs = []
for i in range(5):
    # RG = nx.gnm_random_graph(num_nodes, num_links, seed=None, directed=True)
    RG = nx.gnp_random_graph(num_nodes, (0.1 * i), seed=None, directed=True)
    random_graphs.append(RG)
    nx.write_gml(RG, ("rand" + str(i) + ".gml"))
    plt.figure(figsize=(8, 8))
    nx.draw(RG, node_size=5, alpha=0.5)
    plt.title(f"Random Graph {i}")
    plt.savefig(f'rg{i}.png')
    plt.close()

# Create an Erdos-Renyi graph
# ER = nx.erdos_renyi_graph(num_nodes, num_links/(num_nodes*(num_nodes-1)/2))
ER = nx.erdos_renyi_graph(num_nodes, 0.5, seed=None, directed=True)
nx.write_gml(ER, "erdos-renyi.gml")
plt.figure(figsize=(8, 8))
nx.draw(ER, node_size=5, alpha=0.5)
plt.title('Erdos-Renyi Graph')
plt.savefig('er.png')
plt.close()

## SF

# Scale Free

# Create a Barabasi-Albert graph
BA = nx.barabasi_albert_graph(num_nodes, int(num_links/num_nodes))
nx.write_gml(BA, "barabasi-albert.gml")
plt.figure(figsize=(8, 8))
nx.draw(BA, node_size=5, alpha=0.5)
plt.title('Barabasi-Albert Graph')
plt.savefig('ba.png')
plt.close()

# Print the number of nodes and edges in each graph
print('Original graph: Nodes={}, Edges={}'.format(num_nodes, num_links))
for i, graph in enumerate(random_graphs):
    print('Random graph {} : Nodes={}, Edges={}'.format(i+1, graph.number_of_nodes(), graph.number_of_edges()))
print('Erdos-Renyi graph: Nodes={}, Edges={}'.format(ER.number_of_nodes(), ER.number_of_edges()))
print('Barabasi-Albert graph: Nodes={}, Edges={}'.format(BA.number_of_nodes(), BA.number_of_edges()))

# Target Attack

# Calculate betweenness centrality for all nodes
betweenness = nx.betweenness_centrality(TG)

# Get the 5 nodes with the highest betweenness centrality
top_nodes = sorted(betweenness, key=betweenness.get, reverse=True)[:5]

# Remove the selected nodes
TG.remove_nodes_from(top_nodes)

# Recalculate network parameters
num_nodes = len(TG.nodes)
num_edges = len(TG.edges)
density = nx.density(TG)
avg_clustering_coef = nx.average_clustering(TG)

plt.figure(figsize=(8,8))
nx.draw(TG, node_size=5, alpha=0.5)
plt.title('Graph with 5 highest betweenness centrality nodes deleted')
plt.savefig('bc_deleted_nodes.png')

# Print the new network parameters
print(f'Number of nodes: {num_nodes}')
print(f'Number of edges: {num_edges}')
print(f'Density: {density:.4f}')
print(f'Average clustering coefficient: {avg_clustering_coef:.4f}')

nx.write_gml(TG, "targeted_attack.gml")
