import os
import json
from tabnanny import verbose
from google import genai
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('GEMINI_API_KEY', None)

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=API_KEY)

with open('tests.json', 'r', encoding='utf-8') as f:
    tests = json.load(f)

accuracy = 0; total = 0
for key, value in tests.items():
    patient = value['Consulta']
    diagnostic = value['Diagnóstico']

    medical_prompt = (
        f"Eres un médico clínico. "
        f"A continuación, se te presenta una consulta de un paciente y un diagnóstico inicial. "
        f"Tu tarea es generar un diagnóstico más detallado, inferido o corregido si fuese necesario.\n\n"
        f"Consulta del paciente:\n{patient}\n\n"
        f"Diagnóstico inicial:\n{diagnostic}\n\n"
        f"Diagnóstico final breve (no mas de 50 palabras):"
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=medical_prompt
    )
    
    expected_answer = response.text

    patient_prompt = (
        f"Eres un paciente con las siguientes características: {patient}.\n"
        f"Asistes a una consulta para atender tus padecimientos.\n"
        f"Comenta brevemente tus padecimientos al médico que te atenderá."
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=patient_prompt
    )

    first_message = response.text

    boolean_prompt = (
        f"Actúa como la persona que describes en el siguiente perfil:\n{patient_prompt}\n\n"
        f"Padeces de los siguientes síntomas:\n{patient}\n\n"
        f"Responde únicamente con 1 o 0 a las preguntas médicas relacionadas con estos síntomas."
    )

    final_answer = 'Úlcera venosa en tercio inferior del pie derecho'

    query = 'tienes hambre?'

    followup_response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=boolean_prompt + query
    )
    
    # print(followup_response.text[-1])
    
    accuracy_evaluator_prompt = (
        f"Actúa como un evaluador experto de diagnósticos médicos. "
        f"Evalúa qué tan precisa es la respuesta generada por el sistema (respuesta dada) comparada con la respuesta esperada. "
        f"Usa una escala de 0 a 5, donde:\n"
        f"0 = completamente incorrecta,\n"
        f"1 = muy inexacta,\n"
        f"2 = parcialmente incorrecta,\n"
        f"3 = algo correcta,\n"
        f"4 = mayormente correcta,\n"
        f"5 = completamente correcta.\n\n"
        f"Responde únicamente con un número entero del 0 al 5, sin explicaciones ni texto adicional.\n\n"
        f"Respuesta esperada:\n{expected_answer}\n\n"
        f"Respuesta dada por el sistema:\n{final_answer}\n\n"
        f"Evaluación:"
    )

    response_accuracy = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=accuracy_evaluator_prompt,
    ).text.split()[-1]

    accuracy += int(response_accuracy)
    total += 5

    if total > 30: break

print(accuracy / total)