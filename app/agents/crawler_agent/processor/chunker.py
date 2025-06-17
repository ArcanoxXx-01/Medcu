from typing import Dict
import re

def chunk_sections(secciones: Dict[str, str]):
    """
    Genera frases enriquecidas a partir de las secciones del artículo, con trazabilidad de metadatos.

    Devuelve:
        Lista de tuplas: [chunk_text, metadata = {nombre_usado, causa, sintoma}]
    """
    titulo = secciones.get("titulo", "").strip()
    causas_raw = secciones.get("causas", "")
    sintomas_raw = secciones.get("sintomas", "")
    nombres_alt = secciones.get("nombres_alternativos", "")

    nombres = [titulo] + [n.strip() for n in re.split(r"[;\n]", nombres_alt) if n.strip()]

    causas = [c.strip() for c in causas_raw.split("\n") if c.strip() and not c.strip().endswith(':')]
    sintomas = [s.strip() for s in sintomas_raw.split("\n") if s.strip() and not s.strip().endswith(':')]

    chunks = []
    metadatas = []

    for nombre in nombres:
        for causa in causas:
            texto = f"Una posible causa de {nombre} es {causa}."
            chunks.append(texto)
            metadatas.append({"nombre": nombre, "causa": causa, "sintoma": None})
        for sintoma in sintomas:
            texto = f"{nombre} puede presentar {sintoma}."
            chunks.append(texto)
            metadatas.append({"nombre": nombre, "causa": None, "sintoma": sintoma})
    return [chunks, metadatas]

data = {
    "titulo": "Fractura",
    "causas": "Caída desde una altura\nTraumatismo\nAccidentes automovilísticos",
    "sintomas": "Hinchazón\nDolor intenso",
    "nombres_alternativos": "Hueso roto; Fractura por sobrecarga"
}

for x in chunk_sections(data)[0]:
    print(x)