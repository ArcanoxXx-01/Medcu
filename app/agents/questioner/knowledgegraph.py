<<<<<<< HEAD
<<<<<<< HEAD
import sqlite3

class KnowledgeGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}
=======
from ast import Tuple
=======
>>>>>>> 4a9bfae (All pipeline)
import sqlite3

class KnowledgeGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}
<<<<<<< HEAD
        self.degree = {}
        self.indigree = {}
    
>>>>>>> bf9eccf (Knowledge Graph)
=======
>>>>>>> 4a9bfae (All pipeline)

    def build_graph_from_db(self, db_path: str = "data/embeddings.db"):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print("Construyendo grafo de conocimientos...")
        cursor.execute("SELECT nombre, causa, sintoma FROM vectors")
        for nombre, causa, sintoma in cursor.fetchall():
            try:
                if nombre and nombre not in self.nodes.keys():
<<<<<<< HEAD
<<<<<<< HEAD
                    self.nodes[nombre] = KnowledgeNode('enfermedad')
                    
                if causa and causa not in self.nodes.keys():
                    self.nodes[causa] = KnowledgeNode('causa')
                    
                if sintoma and sintoma not in self.nodes.keys():
                    self.nodes[sintoma] = KnowledgeNode('sintoma')
                    
            except Exception as e: 
                print("Error al crear nodo: ",e)   
            
            try:
                if causa and nombre and tuple([causa, nombre]) in self.edges.keys():
                    self.edges[tuple([causa, nombre])].cost +=1
                    self.edges[tuple([nombre, causa])].cost +=1
                
                if causa and sintoma and tuple([causa, sintoma]) in self.edges.keys():
                    self.edges[tuple([causa, sintoma])].cost +=1
                    self.edges[tuple([sintoma, causa])].cost +=1
                    
                if sintoma and nombre and tuple([sintoma, nombre]) in self.edges.keys():   
                    self.edges[tuple([sintoma, nombre])].cost +=1  
                    self.edges[tuple([nombre, sintoma])].cost +=1  

                      
                if causa and nombre and tuple([causa, nombre]) not in self.edges.keys(): # agregar arista causa-nombre con tipo 'es_causa_de' y peso alto
                    edge_value = 1
                    self.edges[tuple([causa, nombre])] = KnowledgeEdge(edge_value)
                    self.edges[tuple([nombre, causa])] = KnowledgeEdge(edge_value)
                    u = self.nodes[causa]
                    v = self.nodes[nombre]
                    u.outdegree += 1
                    v.indegree += 1 
                            
                if causa and sintoma and tuple([causa, sintoma]) not in self.edges.keys(): # agregar arista causa-sintoma con tipo 'es_causa_de' y peso medio
                    edge_value = 1
                    self.edges[tuple([causa, sintoma])] = KnowledgeEdge(edge_value)
                    self.edges[tuple([sintoma, causa])] = KnowledgeEdge(edge_value)
                    u = self.nodes[causa]
                    v = self.nodes[sintoma]
                    u.outdegree += 1
                    v.indegree +=1 

                if sintoma and nombre and tuple([sintoma, nombre]) not in self.edges.keys(): 
                    edge_value = 1
                    self.edges[tuple([sintoma, nombre])] = KnowledgeEdge(edge_value)
                    self.edges[tuple([nombre, sintoma])] = KnowledgeEdge(edge_value)
                    u = self.nodes[sintoma]
                    v = self.nodes[nombre]
                    u.outdegree += 1
                    u.indegree +=1
                    v.outdegree += 1
                    v.indegree +=1
                    
=======
                    self.nodes[nombre] = KnowledgeNode('enfermedad', self.graph.add_vertex())
=======
                    self.nodes[nombre] = KnowledgeNode('enfermedad')
>>>>>>> 4a9bfae (All pipeline)
                    
                if causa and causa not in self.nodes.keys():
                    self.nodes[causa] = KnowledgeNode('causa')
                    
                if sintoma and sintoma not in self.nodes.keys():
                    self.nodes[sintoma] = KnowledgeNode('sintoma')
                    
            except Exception as e: 
                print("Error al crear nodo: ",e)   
            
            try:
                if causa and nombre and tuple([causa, nombre]) in self.edges.keys():
                    self.edges[tuple([causa, nombre])].cost +=1
                    self.edges[tuple([nombre, causa])].cost +=1
                
                if causa and sintoma and tuple([causa, sintoma]) in self.edges.keys():
                    self.edges[tuple([causa, sintoma])].cost +=1
                    self.edges[tuple([sintoma, causa])].cost +=1
                    
                if sintoma and nombre and tuple([sintoma, nombre]) in self.edges.keys():   
                    self.edges[tuple([sintoma, nombre])].cost +=1  
                    self.edges[tuple([nombre, sintoma])].cost +=1  

                      
                if causa and nombre and tuple([causa, nombre]) not in self.edges.keys(): # agregar arista causa-nombre con tipo 'es_causa_de' y peso alto
                    edge_value = 1
                    self.edges[tuple([causa, nombre])] = KnowledgeEdge(edge_value)
                    self.edges[tuple([nombre, causa])] = KnowledgeEdge(edge_value)
                    u = self.nodes[causa]
                    v = self.nodes[nombre]
                    u.outdegree += 1
                    v.indegree += 1 
                            
                if causa and sintoma and tuple([causa, sintoma]) not in self.edges.keys(): # agregar arista causa-sintoma con tipo 'es_causa_de' y peso medio
                    edge_value = 1
                    self.edges[tuple([causa, sintoma])] = KnowledgeEdge(edge_value)
                    self.edges[tuple([sintoma, causa])] = KnowledgeEdge(edge_value)
                    u = self.nodes[causa]
                    v = self.nodes[sintoma]
                    u.outdegree += 1
                    v.indegree +=1 

                if sintoma and nombre and tuple([sintoma, nombre]) not in self.edges.keys(): 
                    edge_value = 1
                    self.edges[tuple([sintoma, nombre])] = KnowledgeEdge(edge_value)
                    self.edges[tuple([nombre, sintoma])] = KnowledgeEdge(edge_value)
                    u = self.nodes[sintoma]
                    v = self.nodes[nombre]
<<<<<<< HEAD
                    self.graph.add_edge(u.index, v.index, edge_value)
>>>>>>> bf9eccf (Knowledge Graph)
=======
                    u.outdegree += 1
                    u.indegree +=1
                    v.outdegree += 1
                    v.indegree +=1
                    
>>>>>>> 4a9bfae (All pipeline)
            except Exception as e:
                print("Error al crear arista: ", e)   
        conn.close()
        
<<<<<<< HEAD
<<<<<<< HEAD
        print("Grafo de conocimientos construido satisfactoriamente.")
        print(self.summary())
        
    def summary(self):
        return {
            "cantidad de nodos": len(self.nodes),
            "cantidad de aristas": len(self.edges)
        }

class KnowledgeNode:
    def __init__(self, type):
        self.type = type
=======
=======
        print("Grafo de conocimientos construido satisfactoriamente.")
        print(self.summary())
        
>>>>>>> 4a9bfae (All pipeline)
    def summary(self):
        return {
            "cantidad de nodos": len(self.nodes),
            "cantidad de aristas": len(self.edges)
        }

class KnowledgeNode:
    def __init__(self, type):
        self.type = type
<<<<<<< HEAD
        self.index = index
>>>>>>> bf9eccf (Knowledge Graph)
=======
>>>>>>> 4a9bfae (All pipeline)
        self.indegree = 0
        self.outdegree = 0
 
class KnowledgeEdge:
<<<<<<< HEAD
<<<<<<< HEAD
    def __init__(self, cost = 0):
        self.cost = cost   

def process_text(text: str):
    return text.lower().strip().replace('(','').replace(')','')



# ========== Tests =================

# graph = KnowledgeGraph()
# graph.build_graph_from_db()

# for value in graph.edges.values():
#     print(value.cost)


# for node in graph.nodes.keys():
#     if len(node) < 20:
#         print(process_text(node))
#         node = graph.nodes[node]
#         print(f"{node.type}, {node.indegree}, {node.outdegree}")
=======
    def __init__(self, type, cost = 0):
        self.type = type
=======
    def __init__(self, cost = 0):
>>>>>>> 4a9bfae (All pipeline)
        self.cost = cost   

def process_text(text: str):
    return text.lower().strip().replace('(','').replace(')','')


<<<<<<< HEAD
>>>>>>> bf9eccf (Knowledge Graph)
=======

# ========== Tests =================

# graph = KnowledgeGraph()
# graph.build_graph_from_db()

# for value in graph.edges.values():
#     print(value.cost)


# for node in graph.nodes.keys():
#     if len(node) < 20:
#         print(process_text(node))
#         node = graph.nodes[node]
#         print(f"{node.type}, {node.indegree}, {node.outdegree}")
>>>>>>> 4a9bfae (All pipeline)
