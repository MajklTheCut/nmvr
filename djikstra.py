#%%

from matplotlib.pyplot import viridis
import networkx as nx

G = nx.Graph()

G.add_edge("a", "b", weight=6)
G.add_edge("a", "c", weight=2)
G.add_edge("c", "d", weight=1)
G.add_edge("c", "e", weight=7)
G.add_edge("c", "f", weight=9)
G.add_edge("a", "d", weight=3)

pos = nx.spring_layout(G, seed=5)

nx.draw_networkx_nodes(G, pos, cmap= viridis)
nx.draw_networkx_edges(G, pos, width = 3)
# %%
