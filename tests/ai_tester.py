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

    print(first_message)

    query = input()

    followup_response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=boolean_prompt + query
    )
    
    print(followup_response.text[-1])
    