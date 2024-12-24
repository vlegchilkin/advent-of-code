import networkx as nx
import pylab as plt

def draw(graph, outfile):
    pos = nx.spring_layout(graph)
    plt.figure(1, figsize=(48, 48))
    options = {"with_labels": True, "node_size": 1, "font_size": 32}
    nx.draw(graph, pos, **options)
    plt.savefig(outfile)

def draw_neato(graph, outfile, labels = None):
    pos = nx.nx_pydot.graphviz_layout(graph, prog="neato")
    plt.figure(1, figsize=(80, 80))
    options = {"with_labels": True, "node_size": 3, "font_size": 16}
    if labels:
        options["labels"] = labels
    nx.draw(graph, pos, **options)
    plt.savefig(outfile)
