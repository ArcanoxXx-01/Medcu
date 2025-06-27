import csv
import sqlite3
from rapidfuzz import process, fuzz

class KnowledgeGraph:
    def __init__(self, use_db:bool = False, use_csv:bool = False, db_path:str="data/embeddings.db", csv_path:str="data/edges.csv"):
        
        self.nodes: dict[str,Node] = {}
        self.edges: dict[tuple[str,str],Edge] = {}
        
        self.db_path = db_path
        self.csv_path = csv_path
        
        if use_db:
            self.build_by_db()
        if use_csv:
            self.build_by_csv()
        
    def add_node(self, value:str, type:str , points:float = 0):
        """Agrega un nuevo nodo al grafo

        Args:
            value (str): nombre de la entidad que represeta
            type (str): Tiene tres posibles valores: ('sintoma', 'enfermedad', 'causa')
            points (float, optional): peso del nodo. Defaults to 0.
        """
        node = self.nodes[value] if value in self.nodes.keys() else None
        
        if node:
            node.points = points # quedarme con el ultimo peso

            if type not in node.types:
                node.types.append(type)
                
        else:
            self.nodes[value] = Node(value=value, types=[type], points=points)
            
    def add_edge(self, source:str, target:str, type:bool, points:float = 0.5):
        """Agrega una arista al grafo

        Args:
            source (str): valor del nodo de origen (siempre existe)
            target (str): valor del nodo de destino (siempre existe)
            type (bool): True si la arista une un sintom con una enfermedad
            points (float, optional): Peso de la arista. Defaults to 0.
        """
        
        key = tuple([source, target])
        reverse_key = tuple([target, source])
        edge = self.edges[key] if key in self.edges.keys() else None 
        reverse_edge = self.edges[reverse_key] if edge and edge.type else None
        
        if edge:
            edge.points = (edge.points + points)/2
            if type:
                if reverse_edge:
                    reverse_edge.points = (reverse_edge.points + points)/2
                else:
                    self.edges[reverse_key] = Edge(type=type, points=points)
        else:
            self.edges[key] = Edge(type=type, points=points)
            if type:
                self.edges[reverse_key] = Edge(type=type, points=points)
                               
    def build_by_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT nombre, causa, sintoma FROM vectors")
        for nombre, causa, sintoma in cursor.fetchall():
            if nombre:
                self.add_node(value=nombre, type="enfermedad")
                if sintoma:
                    self.add_node(value=sintoma, type="sintoma")
                    self.add_edge(source=sintoma, target=nombre, type=True) 
                if causa:
                    self.add_node(value=causa, type="causa")
                    self.add_edge(source=causa, target=nombre, type=False)

        conn.close()
    
    def build_by_csv(self):
        """Le agrega al grafo las aristas que se encuentran guardadas en el csv que esta en `self.db_path` """
        csv_path = self.csv_path
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                nombre = row.get("nombre", "").strip()
                sintoma = row.get("sintoma", "").strip()
                causa = row.get("causa", "").strip()
                peso = float(row.get("peso", 1.0))

                if nombre:
                    self.add_node(value=nombre, type="enfermedad")
                    if sintoma:
                        self.add_node(value=sintoma, type="sintoma")
                        self.add_edge(source=sintoma, target=nombre, type=True, points=peso)
                    if causa:
                        self.add_node(value=causa, type="causa")
                        self.add_edge(source=causa, target=nombre, type=False, points=peso)
    
    def get_childs(self, node_value:str)->list[str]:
        """Obtiene la lista de nodos que son vecinos del nodo `node_value`

        Args:
            node_value (str): nodo al que se le buscaran los vecinos

        Returns:
            list[str]:lista con los vecinos de `node_value`
        """
        return [x[1] for x in self.edges.keys() if x[0] == node_value]
    
    def get_parents(self, node_value:str)->list[str]:
        """Obtiene la lista de nodos para los cuales `node_value` es vecino 

        Args:
            node_value (str): nodo que debe ser vecino de los nodos a devolver

        Returns:
            list[str]:lista con los nodos que tienen a `node_value` como vecino
        """
        return [x[0] for x in self.edges.keys() if x[1] == node_value]

    def get_related_nodes(self, entities, threshold=85):
        """Devuelve los nodos que superan un umbral de similitud con alguna de las entidades"""
        nodos_grafo = self.nodes.keys()
        nodos_similares = set()

        for entity in entities:
            resultados = process.extract(
                entity,
                nodos_grafo,
                scorer=fuzz.QRatio,
                limit=3
            )
            for nombre, score, _ in resultados:
                if score >= threshold:
                    nodos_similares.add(nombre)

        return list(nodos_similares)
    
    def save_in_csv(self, rows):
        pass
        
    def summary(self):
        print(f"< n_nodes: {len(self.nodes)}, n_edges: {len(self.edges)} >")


class Node:
    """Estructura para los nodos del grafo"""
    def __init__(self, value:str, types:list[str] = [], points:float = 0):
        """
        Args:
            value (str): Nombre de la entidad que representa.
            type (list[str], optional): Contiene los tipos del nodo, que pueden ser: ('causa', 'sintoma', 'enfermedad'). Defaults to [].
            points (float, optional): Peso del nodo (Probabilidad de tenerlo). Defaults to 0.
        """
        self.value = value
        self.types: list[str] = types
        self.points: float = points
        self.lambda_: float = 0

class Edge:
    """Estructura para las aristas del grafo"""
    def __init__(self, type:bool = False, points:float = 0):
        """
        Args:
            type (bool, optional): true si la arista es sintoma<->enfermedad. Defaults to False.
            points (float, optional): peso de la arista. Defaults to 0.
        """
        self.type: bool = type
        self.points: float = points
        
        
# graph = KnowledgeGraph(use_db=False, use_csv=True)
# graph.summary()
