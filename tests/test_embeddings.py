import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.core.embeddings import EmbeddingGenerator
from app.config import EMBEDDING_URL, FIREWORKS_EMBEDDING_MODEL, FIREWORKS_API_KEY
import pytest

# @pytest.mark.skipif(
#     not os.getenv("FIREWORKS_API_KEY"),
#     reason="FIREWORKS_API_KEY no configurada"
# )
# def test_embed_texts_fireworks():
#     # Entradas de prueba
#     textos = ["dolor de cabeza", "fiebre", "mareos intensos"]

#     # Parámetros Fireworks
#     model_id = FIREWORKS_EMBEDDING_MODEL
#     url = EMBEDDING_URL
#     api_key = FIREWORKS_API_KEY

#     generator = EmbeddingGenerator(
#         provider="fireworks",
#         model_id=model_id,
#         api_key=api_key,
#         url=url
#     )

#     # Ejecutar embedding
#     resultado = generator.embed_texts(textos)

#     # Validaciones
#     assert isinstance(resultado, list)
#     assert len(resultado) == len(textos)
#     assert all(isinstance(vec, list) for vec in resultado)
#     assert all(len(vec) > 0 for vec in resultado)

#     print("Embeddings generados correctamente")

def test_embed_minimo():

    generator = EmbeddingGenerator(
        provider="fireworks",
        model_id=FIREWORKS_EMBEDDING_MODEL,
        api_key=FIREWORKS_API_KEY,
        url=EMBEDDING_URL
    )

    textos = ["dolor de cabeza","dolor en las articulaciones"]
    resultado = generator.embed_texts(textos)
    print(resultado)
    assert isinstance(resultado, list)
    assert isinstance(resultado[0]['embedding'], list)
    assert len(resultado) > 0

test_embed_minimo()
