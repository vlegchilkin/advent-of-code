import networkx as nx
import pylab as plt

def draw(graph, outfile):
    pos = nx.spring_layout(graph)
    plt.figure(1, figsize=(48, 48))
    options = {"with_labels": True, "node_size": 1, "font_size": 32}
    nx.draw(graph, pos, **options)
    plt.savefig(outfile)
