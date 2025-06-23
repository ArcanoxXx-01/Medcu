from platform import processor
import time
from typing import Dict
import re
from app.core.processor import FireworksProcessor 

def chunk_sections(secciones: dict, model:FireworksProcessor, retry = 6):
    """
    Genera frases a partir de las secciones del artículo, con trazabilidad de metadatos.

    Devuelve:
        Lista de tuplas: [chunk_text, metadata = {nombre_usado, causa, sintoma}]
    """
    chunks = []
    metadatas = []
    response = None
    for retry in range(retry):
        try:
            response = model.process_entities(secciones)
        except Exception as e:
            wait = 2 ** retry
            print(f"Error (intento {retry+1}/6):\n{e}\nReintentando en {wait}s...")
            time.sleep(wait)
    
    if not response:
        print("Fallo permanente al usar LLM para extraer entidades")
        return [],[]
        
    nombres = [response['enfermedad']]
    nombres.extend(response.get('nombres_alternativos', []))
    causas = response.get('causas', [])
    sintomas = response.get('sintomas', [])
    
    for nombre in nombres:
        
        for causa in causas:
            chunks.append(f"Una posible causa para {nombre} es {causa}")
            metadatas.append({
                'nombre': nombre,
                'sintoma': None,
                'causa': causa
            })
            
        for sintoma in sintomas:
<<<<<<< HEAD
            texto = f"{nombre} puede presentar {sintoma}."
            chunks.append(texto)
            metadatas.append({"nombre": nombre, "causa": None, "sintoma": sintoma})
    return [chunks, metadatas]

# data = {
#     "titulo": "Fractura",
#     "causas": "Caída desde una altura\nTraumatismo\nAccidentes automovilísticos",
#     "sintomas": "Hinchazón\nDolor intenso",
#     "nombres_alternativos": "Hueso roto; Fractura por sobrecarga"
# }

<<<<<<< HEAD
<<<<<<< HEAD
# chunks, metadatas = chunk_sections(data)
# for chunk in chunks:
#     print(chunk)
=======
for x in chunk_sections(data)[0]:
    print(x)
>>>>>>> ef49f87 (add ejemplo_comsulta param to document db)
=======
# chunks, metadatas = chunk_sections(data)
# for chunk in chunks:
#     print(chunk)
>>>>>>> 9e4a382 (Bug fixes in the Crawler)
=======
            chunks.append(f"{nombre} puede presentar el síntoma {sintoma}")
            metadatas.append({
                'nombre': nombre,
                'sintoma': sintoma,
                'causa': None
            })
            
    return chunks, metadatas 
>>>>>>> 1416fff (only the GUI needs to be fixed)
