import unittest
from unittest.mock import patch
from app.core.processor import FireworksProcessor

class TestFireworksProcessor(unittest.TestCase):

    def setUp(self):
        self.processor = FireworksProcessor(model_id="test-model", api_key="test-key")

    @patch("app.core.processor.requests.post")
    def test_limpiar_consulta(self, mock_post):
        # Simulamos la respuesta JSON esperada
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"text": "Consulta limpia de ejemplo"}]
        }

        consulta = "Texto original con errores y muletillas."
        resultado = self.processor.limpiar_consulta(consulta)
        self.assertEqual(resultado, "Consulta limpia de ejemplo")

        # Verificar que se hizo la llamada al API con prompt correcto
        args, kwargs = mock_post.call_args
        self.assertIn("prompt", kwargs["json"])
        # self.assertIn("Consulta original", kwargs["json"]["prompt"] or consulta)
        self.assertIn("Texto original con errores y muletillas.", kwargs["json"]["prompt"])

    @patch("app.core.processor.requests.post")
    def test_extraer_entidades(self, mock_post):
        mock_post.return_value.status_code = 200
        # Respuesta simulada con JSON en string para eval
        mock_post.return_value.json.return_value = {
            "choices": [{"text": "{\"sintomas\": [\"tos\", \"fiebre\"], \"enfermedades\": [\"gripe\"]}"}]
        }

        texto = "Paciente con tos y fiebre."
        entidades = self.processor.extraer_entidades(texto)

        self.assertIn("sintomas", entidades)
        self.assertIn("enfermedades", entidades)
        self.assertListEqual(entidades["sintomas"], ["tos", "fiebre"])
        self.assertListEqual(entidades["enfermedades"], ["gripe"])
    
if __name__ == "__main__":
    unittest.main()