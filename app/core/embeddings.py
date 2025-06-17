from typing import List
import requests

class EmbeddingGenerator:
    def __init__(self, provider: str = "fireworks", model_id: str = "", 
            api_key: str = "",  url: str = "", dimensions: int = 768):
        """_summary_
        
        Args:
            provider (str, optional): _description_. Defaults to "fireworks".
            model_id (str, optional): _description_. Defaults to "".
            api_key (str, optional): _description_. Defaults to "".
            url (str, optional): _description_. Defaults to "".
            dimensions (int, optional): _description_. Defaults to 768.
        """
        self.provider = provider
        self.model_id = model_id
        self.api_key = api_key
        self.dimensions = dimensions
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
            "input": texts,
            "dimensions": self.dimensions
        }

        response = requests.post(self.url, headers=headers, json=payload)

        if response.status_code != 200:
            # print("Payload enviado:", payload)
            print("Error HTTP:", response.status_code)
            print("Respuesta:", response.text)
            response.raise_for_status()

        try:   
            metadatos_embeddings = response.json()["data"]
            
        except (KeyError, ValueError) as e:
            print("Error al parsear la respuesta:", response.text)
            raise e

        return [emb['embedding'] for emb in metadatos_embeddings]
