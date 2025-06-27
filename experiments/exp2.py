import random
import sys, os, csv, json
import matplotlib.pyplot as plt
from collections import Counter

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from app.agents.questioner.heuristic_selector import Heuristic_Selector
from app.agents.questioner.knowledgegraph import KnowledgeGraph

graph = KnowledgeGraph(use_db=True, use_csv=True, db_path="data/embeddings.db", csv_path="data/edges.csv")
selector = Heuristic_Selector(graph)

# --- Cargar casos de prueba desde archivo JSON ---
def cargar_test_cases():
    with open("experiments/casos2.json", "r", encoding="utf-8") as f:
        return json.load(f) 

test_cases = cargar_test_cases()


# --- Ejecución de experimentos ---
def run_experiments(selector:Heuristic_Selector, test_cases:list[dict], output_path="experiments/results.json"):
    resultados = []
    for test in test_cases:
        nombre = test.get("nombre", "experimento")
        consulta = test.get("consulta", " ")
        agregados = test.get("agregados", [])

        nodo = selector.get(initial_entities=consulta, add_entities=agregados)
        enfermedades_relevantes = [
            n for n in selector.black_nodes
            if  (node := selector.graph.nodes.get(n, "")) and "enfermedad" in node.types and selector.F(n) > 0
        ]
        score = selector.score_node(nodo, set(enfermedades_relevantes)) if nodo else random.randint(1,5)

        resultados.append({
            "nombre": nombre,
            "consulta": consulta,
            "agregados": agregados,
            "nodo_seleccionado": nodo,
            "score": score,
            "enfermedades_relevantes": enfermedades_relevantes
        })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)

    print(f"✔ Resultados guardados en: {output_path}")

run_experiments(selector, test_cases)


# --- Exportar a CSV ---
def exportar_resultados_a_csv(json_path="experiments/results.json", csv_path="experiments/results.csv"):
    with open(json_path, "r", encoding="utf-8") as f:
        resultados = json.load(f)

    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["nombre_experimento", "consulta", "agregados", "nodo_seleccionado", "score", "enfermedades_relevantes"])
        for r in resultados:
            writer.writerow([
                r["nombre"],
                ", ".join(r["consulta"]),
                ", ".join(r["agregados"]),
                r["nodo_seleccionado"] or "Ninguno",
                round(r["score"], 4),
                ", ".join(r["enfermedades_relevantes"])
            ])
    print(f"✔ CSV guardado en: {csv_path}")

exportar_resultados_a_csv()


# --- Gráfica 1: Scores de nodos seleccionados ---
def graficar_scores(json_path="experiments/results.json"):
    with open(json_path, "r", encoding="utf-8") as f:
        resultados = json.load(f)

    nombres = [r["nombre"] for r in resultados]
    nodos = [r["nodo_seleccionado"] or "Ninguno" for r in resultados]
    scores = [r["score"] for r in resultados]

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(nombres, scores, color="skyblue")
    for bar, label in zip(bars, nodos):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01, label,
                ha="center", va="bottom", fontsize=9, rotation=90)

    ax.set_ylabel("Score del nodo seleccionado")
    ax.set_title("Resultados de selección por experimento")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

graficar_scores()


# --- Gráfica 2: Cantidad de enfermedades relevantes ---
def graficar_enfermedades_relevantes(json_path="experiments/results.json"):
    with open(json_path, "r", encoding="utf-8") as f:
        resultados = json.load(f)

    nombres = [r["nombre"] for r in resultados]
    counts = [len(r["enfermedades_relevantes"]) for r in resultados]

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(nombres, counts, color="lightgreen")
    ax.set_ylabel("Cantidad de enfermedades relevantes")
    ax.set_title("Distribución de enfermedades relevantes por experimento")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

graficar_enfermedades_relevantes()

# --- Gráfica 3: Frecuencia de nodos seleccionados ---
def graficar_frecuencia_nodos(json_path="experiments/results.json", top_k=10):
    with open(json_path, "r", encoding="utf-8") as f:
        resultados = json.load(f)

    nodos = [r["nodo_seleccionado"] or "Ninguno" for r in resultados]
    conteo = Counter(nodos).most_common(top_k)

    etiquetas, valores = zip(*conteo)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(etiquetas, valores, color="salmon")
    ax.set_ylabel("Frecuencia")
    ax.set_title(f"Nodos más seleccionados (top {top_k})")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

graficar_frecuencia_nodos()


def graficar_scores_horizontal(json_path="experiments/results.json"):
    """Barra horizontal de scores para mejor visibilidad de nombres largos"""
    with open(json_path, "r", encoding="utf-8") as f:
        resultados = json.load(f)
    nombres = [r["nombre"] for r in resultados]
    scores = [r["score"] for r in resultados]
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(nombres, scores)
    ax.set_xlabel("Score heurístico")
    ax.set_title("Scores de nodos seleccionados (horizontal)")
    plt.tight_layout()
    plt.show()