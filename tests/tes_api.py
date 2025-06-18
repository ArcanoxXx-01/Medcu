import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.core.processor import FireworksProcessor
from app.config import API_URL, FIREWORKS_API_KEY, FIREWORKS_MODEL_ID

def test_llamada_real_fireworks():
    processor = FireworksProcessor(model_id=FIREWORKS_MODEL_ID, api_key=FIREWORKS_API_KEY, api_url=API_URL)
    consulta = "Paciente con tos y fiebre desde hace 3 días"
    resultado = processor.limpiar_consulta(consulta)
    print("Resultado limpieza:", resultado)
    entidades = processor.extraer_entidades(resultado)
    print("Entidades extraídas:", entidades)
    
if (__name__ == "__main__"):
    test_llamada_real_fireworks()