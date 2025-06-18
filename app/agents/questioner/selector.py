from .knowledgegraph import KnowledgeGraph

class selector:
  def get(self, start, min_prob = 0.9):
    """
    Given a graph with edge probabilities and a starting vertex, 
    return the next candidate vertices that can be queried in 
    this iteration of the system.
    """
    pass


class ReducerSelector(selector):
  def __init__(self, graph = KnowledgeGraph()):
    super().__init__()
    self.graph = graph
    self.graph.build_graph_from_db()
    
  def get(self, originals_entities: dict = {}, extra_entities:dict = {}):
    """_summary_

    Args:
        originals_entities (dict, optional): _description_. Defaults to {}.
        extra_entities (dict, optional): _description_. Defaults to {}.
    """
    
    black_nodes= []
    for value in originals_entities.values():
        black_nodes.extend(self.get_black_nodes(value))
    
    # print(black_nodes)
    
    cover_nodes= self.get_cover_nodes(black_nodes)
    
    # print(cover_nodes)
    
    gray_nodes= []
    for value in extra_entities.values():
      gray_nodes.extend(self.get_gray_nodes(value, cover_nodes))
      
    # print(gray_nodes)
    
    result = None
    mini = 1e16
    for gray_node in gray_nodes:
      value = self.get_sum_edges(gray_node, cover_nodes)
      if value < mini: 
        result = gray_node
        mini = value
      
    return result
    
  def get_black_nodes (self, entities: list = []):
    return [node for node in self.graph.nodes.keys() if node in entities] 
  
  def get_cover_nodes (self, nodes: list = []):
    V = []
    keys = self.graph.edges.keys()
    for key in keys:
      u,v= key
      if u in nodes:
        V.append(v)
    return V    

  def get_gray_nodes (self, extra_entities= [], V = []):
    gray_nodes=[]
    for key in self.graph.edges.keys():
      u , v = key
      if v in V and u in extra_entities:
        gray_nodes.append(u)
    return gray_nodes 
  
  def get_sum_edges(self, node, cover_nodes):
    result = 0
    for key in self.graph.edges.keys():
      u, v = key
      if u== node and v in cover_nodes:
        result+= self.graph.edges[tuple([u,v])].cost
    
    return result    




# sel = ReducerSelector()
  
# initial = {
#   'symptoms' : ['insomnio', 'dolor de estómago'],
#   'diseases' : ['diabetes']
# }

# extra = {
#   'symptoms' : ['ERT', 'Fatiga' , 'Agotamiento', 'Alergia a los alimentos - huevos'],
# }

# print(sel.get(initial, extra))