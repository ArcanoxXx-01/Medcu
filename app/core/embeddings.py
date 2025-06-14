from typing import List
import os
import requests

class EmbeddingGenerator:
    def __init__(self, provider: str = "fireworks", model_id: str = "", api_key: str = "", url: str = ""):
        self.provider = provider
        self.model_id = model_id
        self.api_key = api_key
        self.url = url
 
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        if self.provider == "fireworks":
            return self._embed_fireworks(texts)
        else:
            raise NotImplementedError("Proveedor de embeddings no soportado aún :)")

    def _embed_fireworks(self, texts: List[str]) -> List[List[float]]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model_id,
            "input": texts
        }

        response = requests.post(self.url, headers=headers, json=payload)

        if response.status_code != 200:
            print("Payload enviado:", payload)
            print("Respuesta completa:", response.text)
            response.raise_for_status()

        return response.json()["data"]

