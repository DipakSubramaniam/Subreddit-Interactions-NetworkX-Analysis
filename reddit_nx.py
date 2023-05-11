# Dipak Subramaniam
# CS 590 SBN Final Project

import networkx as nx
from networkx.algorithms.community import girvan_newman, modularity
import time
import matplotlib.pyplot as plt
import numpy as np
import community
import itertools
import random
from scipy.optimize import curve_fit

G = nx.read_gml('top31subreddits.gml')
print(nx.info(G))

# in out degree histogram
numnodes = G.number_of_nodes()
deg_in = [d for n, d in G.in_degree()]
deg_out = [d for n, d in G.out_degree()]
avg_din = sum(deg_in) / float(numnodes)
avg_dout = sum(deg_out) / float(numnodes)

in_values = sorted(set(deg_in))
in_hist = [deg_in.count(x) for x in in_values]
out_values = sorted(set(deg_out))
out_hist = [deg_out.count(x) for x in out_values]

plt.figure()
plt.plot(in_values, in_hist, 'ro-')  # in-degree
plt.plot(out_values, out_hist, 'bo-')  # out-degree
plt.legend(['In-degree', 'Out-degree'])
plt.xlabel('Degree')
plt.ylabel('Number of nodes')
plt.title('Subreddit Similar Interactions Network')
plt.savefig('in_out_hist_1.png')
plt.close()


# hist 2
in_degrees = [G.in_degree(n) for n in G.nodes()]
out_degrees = [G.out_degree(n) for n in G.nodes()]

plt.hist(in_degrees, alpha=0.5, label='In-degree')
plt.hist(out_degrees, alpha=0.5, label='Out-degree')
plt.xlabel('Degree')
plt.ylabel('Frequency')
plt.legend()
plt.title('Histogram of in/out degree distributions')
plt.savefig('in_out_hist_2.png')
plt.close()

# visualization

# nx.draw_networkx_nodes(G, pos, node_size=node_weights, cmap='seismic')
# nx.draw_networkx_edges(G, pos, edge_color=edge_weights, width=2)
# cbar = plt.colorbar()
# cbar.ax.set_ylabel('Edge weight')
# plt.xlim(-1.1, 1.1)
# plt.ylim(-1.1, 1.1)
# plt.axis('off')
# plt.savefig('reddit_network_vis.png')
# plt.close()

# modifications

edges_to_remove = [(u, v) for u, v, w in G.edges(data='weight') if w < 3.0]
G.remove_edges_from(edges_to_remove)
G.remove_nodes_from(list(nx.isolates(G)))  # removing singletons
nx.write_gml(G, "reddit_filtered.gml")
print(nx.info(G))

betweenness_centrality = nx.betweenness_centrality(G)
degree_centrality = nx.degree_centrality(G)
k = 10
hub_nodes = sorted(degree_centrality, key=degree_centrality.get, reverse=True)[:k]
betweenness = sorted(betweenness_centrality, key=betweenness_centrality.get, reverse=True)[:k]
print("Hub nodes: ", hub_nodes)
print("Hub nodes by betweenness centrality: ", betweenness)

degree_dict = dict(G.degree())  # Get degree for all nodes as a dictionary
sorted_degree = sorted(degree_dict.items(), key=lambda x: x[1], reverse=True)[:10]
bottom = sorted(degree_dict.items(), key=lambda x: x[1], reverse=True)[10:]
# Print out the top 10 degree nodes and their degree values
for node, degree in sorted_degree:
    print(f"{node}: {degree}")
print()
print('bottom')
for node, degree in bottom:
    print(f"{node}: {degree}")

in_degree_dict = dict(G.in_degree())
out_degree_dict = dict(G.out_degree())

print()
sorted_in_degree = sorted(in_degree_dict.items(), key=lambda x: x[1], reverse=True)[:10]
print("Top 10 nodes by in-degree:")
for node, in_degree in sorted_in_degree:
    print(f"{node}: in-degree {in_degree}, out-degree {out_degree_dict[node]}")

sorted_in_degree = sorted(in_degree_dict.items(), key=lambda x: x[1])[:10]
print("\nBottom 10 nodes by in-degree:")
for node, in_degree in sorted_in_degree:
    print(f"{node}: in-degree {in_degree}, out-degree {out_degree_dict[node]}")

sorted_out_degree = sorted(out_degree_dict.items(), key=lambda x: x[1], reverse=True)[:10]
print("\nTop 10 nodes by out-degree:")
for node, out_degree in sorted_out_degree:
    print(f"{node}: in-degree {in_degree_dict[node]}, out-degree {out_degree}")

sorted_out_degree = sorted(out_degree_dict.items(), key=lambda x: x[1])[:10]
print("\nBottom 10 nodes by out-degree:")
for node, out_degree in sorted_out_degree:
    print(f"{node}: in-degree {in_degree_dict[node]}, out-degree {out_degree}")

betweenness_dict = nx.betweenness_centrality(G)
betweenness_sorted = sorted(betweenness_dict.items(), key=lambda x: x[1], reverse=True)[:10]
print("\nTop 10 nodes by betweenness centrality:")
for b in betweenness_sorted:
    print(b[0], ":", b[1], "in degree:", G.in_degree(b[0]), "out degree:", G.out_degree(b[0]))

# charts
# Degree distribution chart
degrees = sorted([d for n, d in G.degree()], reverse=True)
degree_counts = [(i, degrees.count(i)) for i in range(max(degrees) + 1)]
x, y = zip(*degree_counts)
plt.scatter(x, y)
plt.xscale("log")
plt.yscale("log")
plt.xlabel("Degree")
plt.ylabel("Frequency")
plt.title("Degree Distribution")
plt.savefig('degdist.png')
plt.show()
plt.close()

# calculate in-degree and out-degree
# in_degrees = dict(G.in_degree())
# out_degrees = dict(G.out_degree())

in_degrees = [deg for _, deg in G.in_degree()]
out_degrees = [deg for _, deg in G.out_degree()]

# Plot the distributions on a log-log scale
fig, ax = plt.subplots(2, 1, figsize=(8, 8))
ax[0].hist(in_degrees, bins=50, log=True)
ax[0].set_xscale('log')
ax[0].set_yscale('log')
ax[0].set_xlabel('In-Degree')
ax[0].set_ylabel('Frequency')

ax[1].hist(out_degrees, bins=50, log=True)
ax[1].set_xscale('log')
ax[1].set_yscale('log')
ax[1].set_xlabel('Out-Degree')
ax[1].set_ylabel('Frequency')
plt.savefig('in out deg dist.png')
plt.show()
plt.close()

# Plot the distributions on a log-log scale
fig, ax = plt.subplots(2, 1, figsize=(8, 8))
ax[0].scatter(sorted(set(in_degrees)), [in_degrees.count(i) for i in sorted(set(in_degrees))], s=30, c='blue')
ax[0].set_xscale('log')
ax[0].set_yscale('log')
ax[0].set_xlabel('In-Degree')
ax[0].set_ylabel('Frequency')

ax[1].scatter(sorted(set(out_degrees)), [out_degrees.count(i) for i in sorted(set(out_degrees))], s=30, c='red')
ax[1].set_xscale('log')
ax[1].set_yscale('log')
ax[1].set_xlabel('Out-Degree')
ax[1].set_ylabel('Frequency')
plt.savefig('in out deg dist 2.png')
plt.show()
plt.close()


# Betweenness centrality distribution
betweenness_values = sorted(nx.betweenness_centrality(G).values(), reverse=True)
betweenness_counts = [(i, betweenness_values.count(i)) for i in set(betweenness_values)]
x, y = zip(*betweenness_counts)
plt.scatter(x, y)
plt.xlabel("Betweenness Centrality")
plt.ylabel("Frequency")
plt.title("Betweenness Centrality Distribution")
plt.savefig('bcdist.png')
plt.show()
plt.close()

# Closeness centrality distribution
closeness_values = sorted(nx.closeness_centrality(G).values(), reverse=True)
closeness_counts = [(i, closeness_values.count(i)) for i in set(closeness_values)]
x, y = zip(*closeness_counts)
plt.scatter(x, y)
plt.xlabel("Closeness Centrality")
plt.ylabel("Frequency")
plt.title("Closeness Centrality Distribution")
plt.savefig('ccdist.png')
plt.show()
plt.close()


# Clustering coefficient distribution
clustering_values = sorted(nx.clustering(G).values(), reverse=True)
clustering_counts = [(i, clustering_values.count(i)) for i in set(clustering_values)]
x, y = zip(*clustering_counts)
plt.scatter(x, y)
plt.xlabel("Clustering Coefficient")
plt.ylabel("Frequency")
plt.title("Clustering Coefficient Distribution")
plt.savefig('clustcoeff.png')
plt.show()
plt.close()

# Girvan-Newman clustering
gn_communities = nx.community.girvan_newman(G)
gn_colors = {}
gn_num_communities = 0
for communities in itertools.islice(gn_communities, 0, 1):
    gn_num_communities = len(communities)
    for i, community in enumerate(communities):
        for node in community:
            gn_colors[node] = i / float(len(communities) - 1)
nx.draw(G, cmap=plt.get_cmap('viridis'), node_color=list(gn_colors.values()))
plt.title(f"Girvan-Newman Clustering ({gn_num_communities} communities)")
print(f"comm: {gn_num_communities}")
plt.savefig('gn-clust.png')
plt.show()
plt.close()

# Louvain clustering
# for u, v, data in G.edges(data=True):
#     for attr_name in data.keys():
#         if data[attr_name] is None:
#             print(f"Edge ({u}, {v}) has missing value for attribute '{attr_name}'")
#
# for node, data in G.nodes(data=True):
#     for attr_name in data.keys():
#         if data[attr_name] is None:
#             print(f"Node {node} has missing value for attribute '{attr_name}'")
# lv_communities = nx.community.greedy_modularity_communities(G)
# lv_community_colors = {}
# lv_community_count = 0
# for community in lv_communities:
#     for node in community:
#         lv_community_colors[node] = lv_community_count
#     lv_community_count += 1
# nx.draw(G, cmap=plt.get_cmap("tab20"), node_color=[lv_community_colors[node] for node in G.nodes()])
# plt.title("Louvain Clustering ({} communities)".format(lv_community_count))
# plt.savefig('louvain.png')
# plt.show()
# plt.close()

# attack

#original
plt.figure(figsize=(8,8))
nx.draw(G, node_size=5, alpha=0.5)
plt.title('Original graph')
plt.savefig('original_graph.png', dpi=300)

# Randomly select 5 nodes to remove
nodes_to_remove = random.sample(list(G.nodes), 5)
RG = G
TG = G

# Remove the selected nodes
RG.remove_nodes_from(nodes_to_remove)

# Recalculate network parameters
num_nodes = len(RG.nodes)
num_edges = len(RG.edges)
density = nx.density(RG)
avg_clustering_coef = nx.average_clustering(RG)

plt.figure(figsize=(8,8))
nx.draw(G, node_size=5, alpha=0.5)
plt.title('Graph with 5 randomly deleted nodes')
plt.savefig('random_deleted_nodes.png')

# Print the new network parameters
print(f'Number of nodes: {num_nodes}')
print(f'Number of edges: {num_edges}')
print(f'Density: {density:.4f}')
print(f'Average clustering coefficient: {avg_clustering_coef:.4f}')

nx.write_gml(RG, "random_attack.gml")

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