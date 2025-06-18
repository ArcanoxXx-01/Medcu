from app.agents.questioner.knowledgegraph import KnowledgeGraph
from app.agents.questioner.selector import ReducerSelector


class Diagnostician:
    def __init__(self):
        self.selector = ReducerSelector()
    
    def diagnose(self, entities: dict = {}):
        
        black_nodes = []
        for entity in entities:
            black_nodes.extend(self.selector.get_black_nodes(entity))
            
        cover_nodes= self.selector.get_cover_nodes(black_nodes)
        
        best_node = None
        max_value = 0
        
        for node in cover_nodes:
            for values in entities.values():
                if node not in values and self.selector.graph.nodes[node].type != "causa":
                    summa = self._get_sum_edges(cover_nodes, black_nodes)
                    if summa > max_value:
                        best_node = node
                        max_value = summa
        return best_node
                    
    def _get_sum_edges(self, node, black_nodes):
        result = 0
        for key in self.selector.graph.edges.keys():
            u, v = key
            if u == node and v in black_nodes:
                result += self.selector.graph.edges[tuple([u,v])].cost
        return result
    
