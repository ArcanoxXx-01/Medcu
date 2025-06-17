from ast import Tuple
import sqlite3
from .digraph import digraph

class KnowledgeGraph:
    def __init__(self):
        self.graph = digraph()
        self.nodes = {}
        self.edges = {}
        self.degree = {}
        self.indigree = {}
    

    def build_graph_from_db(self, db_path: str = "data/embeddings.db"):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print("Construyendo grafo de conocimientos...")
        cursor.execute("SELECT nombre, causa, sintoma FROM vectors")
        for nombre, causa, sintoma in cursor.fetchall():
            try:
                if nombre and nombre not in self.nodes.keys():
                    self.nodes[nombre] = KnowledgeNode('enfermedad', self.graph.add_vertex())
                    
                if causa and causa not in self.nodes.keys():
                    self.nodes[causa] = KnowledgeNode('causa', self.graph.add_vertex())
                    
                if sintoma and sintoma not in self.nodes.keys():
                    self.nodes[sintoma] = KnowledgeNode('sintoma', self.graph.add_vertex())
            except Exception as e: 
                print("Error al crear nodo: ",e)   
            try:
                if causa and nombre and Tuple([causa, nombre]) not in self.edges.keys(): # agregar arista causa-nombre con tipo 'es_causa_de' y peso alto
                    edge_value = 0.9
                    self.edges[Tuple([causa, nombre])] = KnowledgeEdge('es_causa_de', edge_value)
                    u = self.nodes[causa]
                    v = self.nodes[nombre]
                    self.graph.add_edge(u.index, v.index, edge_value)
                            
                if causa and sintoma and Tuple([causa, sintoma]) not in self.edges.keys(): # agregar arista causa-sintoma con tipo 'es_causa_de' y peso medio
                    edge_value = 0.9
                    self.edges[Tuple([causa, sintoma])] = KnowledgeEdge('es_causa_de', edge_value)
                    u = self.nodes[causa]
                    v = self.nodes[sintoma]
                    self.graph.add_edge(u.index, v.index, edge_value)

                if sintoma and nombre and Tuple([sintoma, nombre]) not in self.edges.keys(): # agregar arista sintoma-nombre con tipo 'es_sintoma_de' y peso variable
                    edge_value = 0.9
                    self.edges[Tuple([sintoma, nombre])] = KnowledgeEdge('es_sintoma_de', edge_value)
                    u = self.nodes[sintoma]
                    v = self.nodes[nombre]
                    self.graph.add_edge(u.index, v.index, edge_value)
            except Exception as e:
                print("Error al crear arista: ", e)   
        conn.close()
        
    def summary(self):
        return {
            "n_nodes": len(self.nodes),
            "n_edges": len(self.edges)
        }

class KnowledgeNode:
    def __init__(self, type, index):
        self.type = type
        self.index = index
        self.indegree = 0
        self.outdegree = 0
 
class KnowledgeEdge:
    def __init__(self, type, cost = 0):
        self.type = type
        self.cost = cost   

graph = KnowledgeGraph()
graph.build_graph_from_db()

print(graph.summary())


