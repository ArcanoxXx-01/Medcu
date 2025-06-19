import requests
from app.core.prompts import *

class FireworksProcessor:
    """
    Clase para interactuar con los modelos de Fireworks.ai para procesamiento de texto médico.

    Métodos:
    - limpiar_consulta(consulta): Limpia y mejora el texto de la consulta médica.
    - extraer_entidades(texto): Extrae síntomas y enfermedades en formato JSON.
    """

    def __init__(self, model_id: str, api_key: str, api_url: str):
        """
        Inicializa el procesador con el ID del modelo, clave API y URL de la API.

        Args:
            model_id (str): Identificador del modelo Fireworks (chat).
            api_key (str): Clave de API para autenticación.
            api_url (str): URL del endpoint de chat completions (ej: https://api.fireworks.ai/inference/v1/chat/completions).
        """
        self.api_url = api_url
        self.model_id = model_id
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _llm_request(self, prompt: str, temperature: float = 0.2) -> str:
        """
        Realiza la solicitud HTTP al modelo Fireworks tipo chat con un prompt dado.

        Args:
            prompt (str): Texto que se envía como mensaje de usuario.
            temperature (float, opcional): Controla la creatividad de la respuesta. Por defecto 0.2.

        Returns:
            str: Texto generado por el modelo.

        Raises:
            Exception: Si la respuesta HTTP no es exitosa.
        """
        data = {
            "model": self.model_id,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": 512,
            "stop": ["</END>"]
        }

        response = requests.post(self.api_url, json=data, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Error en Fireworks API: {response.status_code}, {response.text}")
        
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()

    def limpiar_consulta(self, consulta: str) -> str:
        """
        Limpia la consulta médica eliminando palabras irrelevantes, muletillas y errores.

        Args:
            consulta (str): Texto de la consulta original del usuario.

        Returns:
            str: Texto limpio y mejorado, listo para procesamiento posterior.
        """
        prompt = LIMPIAR_CONSULTA.format(consulta=consulta)
        return self._llm_request(prompt)

    def extraer_entidades(self, texto: str) -> dict:
        """
        Extrae síntomas y enfermedades de un texto médico.

        Args:
            texto (str): Texto limpio o consulta médica procesada.

        Returns:
            dict: Diccionario con claves 'sintomas' y 'enfermedades', cada una con listas de entidades extraídas.

        Raises:
            ValueError: Si la extracción falla o el formato no es correcto.
        """
        prompt = EXTRAER_ENTIDADES.format(texto=texto)

        try:
            output = self._llm_request(prompt).strip()

            if output.startswith("```") or output.endswith("```"):
                output = output.split("```")[1].strip()
            if output.startswith("json"):
                output = output.split("json")[1].strip()
                
            entidades = eval(output, {"__builtins__": {}})
            if not isinstance(entidades, dict):
                raise ValueError("La salida no es un diccionario.")
            return dict({
                "sintomas": entidades.get("sintomas", []),
                "enfermedades": entidades.get("enfermedades", [])
            })
        except Exception as e:
            raise ValueError(f"Error al extraer entidades: {e}\nSalida obtenida: {output}")
        
    def generate_diagnostic(self, diagnostico, entidades):
        prompt = GENERATE_DIAGNOSTIC.format(diagnostico=diagnostico, entidades=entidades)
        try:
            output = self._llm_request(prompt).strip()
            return output
        except Exception as e:
            raise ValueError(f"Error al generar texto del diagnóstico: {e}\nPrompt usado: {prompt}")

    def generate_question(self, entidad):
        prompt = GENERATE_QUESTION.format(entidad=entidad)
        try:
            output = self._llm_request(prompt).strip()
            return output
        except Exception as e:
            raise ValueError(f"Error al generar pregunta de feedback: {e}\nPrompt usado: {prompt}")