import math
import random
from .selector import selector, KnowledgeGraph

class Heuristic_Selector(selector):
    def __init__(self, graph:KnowledgeGraph):
        super().__init__()
        self.graph = graph
        self.black_nodes = []
        self.gray_nodes = []
        self.relevants:list[tuple[str,float]] = []
        self.assign_lambda_to_diseases()
        
    def get(self, initial_entities:list[str], add_entities:list[str]=[]):
        
        self.black_nodes = initial_entities
        self.gray_nodes = add_entities
        # print(f"Black: {self.black_nodes},\nGray: {self.gray_nodes}\n")

        # Calcular F para black_nodes (solo enfermedades)
        
        F_distr = []
        for n in self.black_nodes:
            f = self.F(n)
            F_distr.append((n, f))     
        
        if not F_distr:
            return None
        
        # print("F_distr: ", F_distr)
        # Punto de corte como promedio
        F_sum = sum(f for _, f in F_distr)
        # print("F_sum: ", F_sum)
        cut_point = F_sum / len(F_distr)
        # print("cut_point: ", cut_point)
        
        # Enfermedades con F >= promedio
        F_upper = [n for n, f in F_distr if f >= cut_point]
        # print("F_upper: ", F_upper)
        
        # Buscar nodos conectados hacia atrás desde F_upper
        search_space = {
            parent for node in F_upper
                        for parent in self.graph.get_parents(node)
                            if parent not in self.black_nodes
        }

        # Reducir el espacio a los gray_nodes conocidos
        # search_space &= set(self.gray_nodes)
        # for x in search_space:
        #     print(x)
        
        if not search_space:
            return None

        relevants = set(F_upper)
        # print("relevants: ", relevants)
        
        best = max(search_space, key=lambda n: self.score_node(n, relevants))
        
        return best 
    
    def assign_lambda_to_diseases(self, low: float = 0.01, high: float = 2.0):
        """Asigna un valor lambda simulado a cada enfermedad del grafo.

        Args:
            low (float): valor mínimo de lambda
            high (float): valor máximo de lambda
        """
        for node in self.graph.nodes.values():
            if "enfermedad" in node.types:
                node.lambda_ = random.uniform(low, high)   
        
    def P(self, entitie:str) -> float:
        """Devuelve la probabilidad de tener una entidad
        *(de momento solo lo hacemos para las enfermedades, el resto de entidades le damos peso 0)

        Args:
            entitie (str): entidad medica (causa, sintoma o enfermedad)

        Returns:
            float: probabilidad de tener la entidad
        """
        node = self.graph.nodes.get(entitie, None)
        
        if node and "enfermedad" in node.types:
            
            λ = node.lambda_ if hasattr(node, "lambda_") else 1
            return 1 - math.exp(-λ)
        return 0
        
    def F(self, entitie:str) -> float:
        """Devuelve el peso actual de una entidad (0 si no es una enfermedad)

        Args:
            entitie (str): entidad (causa, sintoma o enfermedad)

        Returns:
            float: peso de la entidad
        """  
        sum = 0
        p = self.P(entitie)
        
        if p > 0:
            for node in self.black_nodes:
                key = tuple([node, entitie])
                if key in self.graph.edges.keys():
                    sum += self.graph.edges[key].points
            return sum * p
        else:
            return 0
    
    def score_node(self, node: str, relevants_nodes: set[str]) -> float:
        """Calcula cuánto contribuye un nodo a las enfermedades relevantes"""
        childs = self.graph.get_childs(node)
        
        if not childs:
            return 0

        relevant_sum = 0
        total_sum = 0

        for child in childs:
            key = (node, child)
            if key in self.graph.edges:
                peso = self.graph.edges[key].points
                total_sum += peso
                if child in relevants_nodes:
                    relevant_sum += peso

        if total_sum == 0:
            return 0

        return relevant_sum / total_sum
    
    def infer_diagnostic(self, new_black_nodes):
        self.black_nodes = new_black_nodes
        
        F_distr = [
            [f, n] for n in self.black_nodes
            if (f := self.F(n)) > 0
        ] 
        
        F_distr.sort(reverse=True)
        return F_distr[0:5]

# graph = KnowledgeGraph(use_csv=True)
# heur = Heuristic_Selector(graph=graph)

# print(heur.P("migraña"))
