import sqlite3
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import csv
import pickle
import json
from rapidfuzz import process, fuzz

class MedicalGraphBuilder:
    def __init__(self, db_path: str = "data/embeddings.db"):
        self.db_path = db_path
        self.graph = nx.DiGraph()
        self.add_edges_from_csv()
        self.build_graph()

    def build_graph(self):
        """Construir el grafo
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT nombre, causa, sintoma FROM vectors")
        for nombre, causa, sintoma in cursor.fetchall():
            if nombre:
                if sintoma:
                    self._add_edge(sintoma.strip(), nombre.strip(), tipo="sintoma")
                if causa:
                    self._add_edge(causa.strip(), nombre.strip(), tipo="causa")

        conn.close()

    def _add_edge(self, source, target, tipo, peso=1.0):
        """Agregar arista"""
        if self.graph.has_edge(source, target):
            self.graph[source][target]['peso'] += peso
        else:
            self.graph.add_edge(source, target, tipo=tipo, peso=peso)


    def add_edges_from_csv(self, csv_path: str = 'data/edges.csv'):
        """Agregar aristas de un csv"""
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                nombre = row.get("nombre", "").strip()
                sintoma = row.get("sintoma", "").strip()
                causa = row.get("causa", "").strip()
                peso = float(row.get("peso", 1.0))

                if nombre:
                    if sintoma:
                        self._add_edge(sintoma, nombre, tipo="sintoma", peso=peso)
                    if causa:
                        self._add_edge(causa, nombre, tipo="causa", peso=peso)

    def visualize(self):
        """Dibuja el grafo con matplotlib (no ponerle muchas aristas al grafo xq se demora demasiado)"""
        pos = nx.spring_layout(self.graph, seed=42)
        edge_labels = nx.get_edge_attributes(self.graph, 'tipo')
        weights = [self.graph[u][v]['peso'] for u, v in self.graph.edges]

        plt.figure(figsize=(12, 8))
        nx.draw(self.graph, pos, with_labels=True, node_color='lightblue', edge_color='gray', width=weights)
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)
        plt.title("Grafo Médico: síntomas y causas hacia enfermedades")
        plt.show()

    def save_graph(graph: nx.DiGraph, path: str, pickle_format: bool = False, json_format: bool = False):
        """Guarda el grafo en disco con distintas opciones de formato"""
        if pickle_format:
            with open(path + ".pkl", "wb") as f:
                pickle.dump(graph, f)

        if json_format:
            data = nx.node_link_data(graph)
            with open(path + ".json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

    def load_graph(path: str, pickle_format: bool = False, json_format: bool = False) -> nx.DiGraph:
        """Carga un grafo previamente guardado en disco"""
        if pickle_format:
            with open(path + ".pkl", "rb") as f:
                return pickle.load(f)

        if json_format:
            with open(path + ".json", "r", encoding="utf-8") as f:
                data = json.load(f)
                return nx.node_link_graph(data)

        raise ValueError("Debe especificar al menos un formato para cargar el grafo.")

    def infer_diagnosis(self, observed_symptoms):
        """Metodo de diagnostico basico (suma de peso de aristas)"""
        scores = defaultdict(float)

        for symptom in observed_symptoms:
            for succ in self.graph.successors(symptom):
                edge = self.graph[symptom][succ]
                if edge['tipo'] == 'sintoma':
                    scores[succ] += edge['peso']

        sorted_diagnosis = sorted(scores.items(), key=lambda x: -x[1])
        return sorted_diagnosis

    def sugerir_pregunta_feedback(self, nodos_negros, nodos_grises):
        """Selecciona el nodo que mas presicion aporta para preguntarle al usuario si lo posee"""
        def calcular_ganancia(original, modificado):
            top1_orig = original[0][1] if original else 0
            top1_mod = modificado[0][1] if modificado else 0
            return top1_mod - top1_orig

        originales = self.infer_diagnosis(nodos_negros)
        mejor_nodo = None
        mejor_ganancia = float('-inf')

        for nodo in nodos_grises:
            if nodo in nodos_negros:
                continue

            nuevos = nodos_negros + [nodo]
            nuevos_diagnosticos = self.infer_diagnosis(nuevos)
            ganancia = calcular_ganancia(originales, nuevos_diagnosticos)

            if ganancia > mejor_ganancia:
                mejor_ganancia = ganancia
                mejor_nodo = nodo

        return mejor_nodo

    def obtener_nodos_asociados(self, entidades, threshold=85):
        """Devuelve los nodos que superan un umbral de similitud con alguna de las entidades"""
        nodos_grafo = list(self.graph.nodes)
        nodos_similares = set()

        for entidad in entidades:
            resultados = process.extract(
                entidad,
                nodos_grafo,
                scorer=fuzz.QRatio,
                limit=3
            )
            for nombre, score, _ in resultados:
                if score >= threshold:
                    nodos_similares.add(nombre)

        return list(nodos_similares)

# graph = MedicalGraphBuilder()
# graph.visualize()
