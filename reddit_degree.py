import networkx as nx
import matplotlib.pyplot as plt

# directed in out degree hist
def dir_deg_hist(G, ind=False, outd=False):
    nodes = G.nodes()
    if ind:
        ind = dict(G.in_degree())
        degseq = [ind.get(k,0) for k in nodes]
    elif outd:
        outd = dict(G.out_degree())
        degseq = [outd.get(k,0) for k in nodes]
    else:
        degseq = [v for k, v in G.degree()]
    dmax = max(degseq)+1
    freq = [0 for d in range(dmax)]
    for d in degseq:
        freq[d] += 1
    return freq

G = nx.read_gml('reddit_filtered.gml')

G = nx.scale_free_graph(5000)

in_degree_freq = dir_deg_hist(G, ind=True)
out_degree_freq = dir_deg_hist(G, outd=True)
degrees = range(len(in_degree_freq))
plt.figure(figsize=(12, 8))
plt.loglog(range(len(in_degree_freq)), in_degree_freq, 'go-', label='in-degree')
plt.loglog(range(len(out_degree_freq)), out_degree_freq, 'bo-', label='out-degree')
plt.legend(loc="upper right")
plt.title('Histogram of in/out degree distributions')
plt.xlabel('Degree')
plt.ylabel('Frequency')
plt.savefig('in_out_hist_3.png')
plt.close()
