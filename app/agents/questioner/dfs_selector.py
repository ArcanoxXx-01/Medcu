from digraph import *
from selector import selector

class dfs_selector(selector):
  def __init__(self, graph: digraph):
    super().__init__(graph)
  
  def get(self, start, min_prob = 0.9):
    result = []
    visited = [False for i in range(self.graph.V)]
    def dfs(u, prob = 1.0):
      visited[u] = True
      if prob < min_prob:
        result.append([u, prob])
        return

      for edge_id in self.graph.G[u]:
        _, v, p = self.graph.E[edge_id]
        if visited[v]: continue
        dfs(v, prob * p)

    dfs(start)
    return result

# g = digraph(6)
# g.add_edge(1, 2, 0.95)
# g.add_edge(2, 3, 0.7)
# g.add_edge(1, 5, 0.35)
# g.add_edge(1, 4, 1)
# g.add_edge(4, 5, 0.8)
# g.add_edge(5, 3, 0.8)
# g.add_edge(5, 2, 0.9)

# select = dfs_selector(g)
# print(select.get(1))