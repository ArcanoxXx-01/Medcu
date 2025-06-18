class digraph:
  def __init__(self, V = 0):
    self.V = V
    self.E = []
    self.G = [[] for _ in range(V)]

  def add_vertex(self):
    self.V += 1
    self.G.append([])
    return self.V - 1
  
  def add_edge(self, u, v, w):
    assert 0 <= u and u < self.V and 0 <= v and v < self.V
    id = len(self.E)
    self.G[u].append(id)
    self.E.append([u, v, w])
    return id
  
  def reverse(self):
    rev = digraph(self.V)
    for e in self.E:
      rev.add_edge(e[1], e[0], e[2])
    return rev