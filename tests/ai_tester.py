import json
from tabnanny import verbose
import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/")))
from app.core.embeddings import EmbeddingGenerator

from console_app import Asisstant
from app.core.processor import FireworksProcessor
from app.config import *
# load_dotenv()
# API_KEY = os.getenv('FIREWORKS_API_KEY', None)

# if not API_KEY:
#     raise ValueError("GEMINI_API_KEY not found in .env")

# client = genai.Client(api_key=API_KEY)

class Tester(Asisstant):
    def __init__(self):
        super().__init__()
        self.answer = ''
        self.boolean_prompt = ''
 
        self.llm = FireworksProcessor(
            model_id=FIREWORKS_MODEL_ID,
            api_key=FIREWORKS_API_KEY,
            api_url=API_URL
        )

    def generar_respuesta_error(self, mensaje):
        pass

    def generar_respuesta_diagnostico(self, diagnostico, entidades):
        self.answer = self.process_model.generate_diagnostic(diagnostico, entidades)
        
    def gen_boolean_prompt(self, patient, patient_prompt):
        self.boolean_prompt = (
            f"Actúa como la persona que describes en el siguiente perfil:\n{patient_prompt}\n\n"
            f"Padeces de los siguientes síntomas:\n{patient}\n\n"
            f"Responde únicamente con 1 o 0 a las preguntas médicas relacionadas con estos síntomas."
        )

    def preguntar_usuario(self, question):
        response = self.llm._llm_request(self.boolean_prompt + question, temperature=0.1)
        # response = client.models.generate_content(
        #     model="gemini-2.5-flash",
        #     contents=self.boolean_prompt + question
        # )

        self.confirmation = response[-1] == '1'

    def test(self):
        with open('tests/tests.json', 'r', encoding='utf-8') as f:
            tests = json.load(f)

        accuracy = 0; cnt_tests = 0
        for key, value in tests.items():
            patient = value['Consulta']
            diagnostic = value['Diagnóstico']

            medical_prompt = (
                f"Eres un médico clínico. "
                f"A continuación, se te presenta una consulta de un paciente y un diagnóstico inicial. "
                f"Tu tarea es generar un diagnóstico más detallado, inferido o corregido si fuese necesario.\n\n"
                f"Consulta del paciente:\n{patient}\n\n"
                f"Diagnóstico inicial:\n{diagnostic}\n\n"
                f"Diagnóstico final:"
            )
            
            while True:
                try:
                    response = self.llm._llm_request(medical_prompt, temperature=0.0)
                    break
                except:
                    time.sleep(20)
                    continue
            # response = client.models.generate_content(
            #     model="gemini-2.5-flash",
            #     contents=medical_prompt
            # )
            
            expected_answer = response

            patient_prompt = (
                f"Eres un paciente con las siguientes características: {patient}.\n"
                f"Asistes a una consulta para atender tus padecimientos.\n"
                f"Comenta brevemente tus padecimientos al médico que te atenderá."
            )
            
            while True:
                try:
                    response = self.llm._llm_request(patient_prompt, temperature=0.4)
                    break
                except:
                    time.sleep(20)
                    continue
            
            # response = client.models.generate_content(
            #     model="gemini-2.5-flash",
            #     contents=patient_prompt
            # )

            first_message = response

            self.gen_boolean_prompt(patient, patient_prompt)
            self.orchestrator.diagnosticar(first_message)

            evaluator_prompt = (
                f"Actúa como un evaluador médico experto. "
                f"Tu tarea es calificar la calidad del diagnóstico realizado por un doctor comparándolo con un diagnóstico esperado. "
                f"El resultado debe ser un único número entero entre 0 y 5. No incluyas texto adicional ni explicaciones; responde solo con el entero.\n"
                f"Escala de puntuación:\n"
                f"5: Diagnóstico completamente correcto, preciso y bien argumentado.\n"
                f"4: Diagnóstico mayormente correcto, con pequeños errores u omisiones.\n"
                f"3: Diagnóstico parcialmente correcto; incluye elementos clave pero también errores importantes.\n"
                f"2: Diagnóstico en su mayoría incorrecto, aunque con alguna idea vaga relacionada.\n"
                f"1: Diagnóstico equivocado, sin relación clara con el caso, pero sin riesgos críticos.\n"
                f"0: Diagnóstico completamente incorrecto y potencialmente peligroso.\n\n"
                f"Diagnóstico esperado: {expected_answer}\n"
                f"Diagnóstico a evaluar: {self.answer}\n"
                f"Respuesta (solo el entero 0 y 5): "
            )

            # print(evaluator_prompt)
            while True:
                try:
                    response = self.llm._llm_request(evaluator_prompt, temperature=0.8)
                    break
                except:
                    time.sleep(20)
                    continue
            
            # response = client.models.generate_content(
            #     model="gemini-2.5-flash",
            #     contents=evaluator_prompt
            # )          
            accuracy += int(response.split()[-1])
            cnt_tests += 5
            print(accuracy)
            print("expected:", expected_answer)
            print("found:", self.answer)

        return accuracy / cnt_tests

tester = Tester() 
tester.test()