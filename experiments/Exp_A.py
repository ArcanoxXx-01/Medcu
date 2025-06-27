import sys, os, time, csv, json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from console_app import Asisstant as Assistant
from app.core.processor import FireworksProcessor
from app.config import *


# 🧪 Plan de Experimentos – Medicub

## Objetivo General
# Evaluar la precisión del diagnóstico, la utilidad de la recuperación semántica, 
# la efectividad de las preguntas aclaratorias y el rendimiento del sistema completo.

class ExpA(Assistant):
    """Simula las consultas de los casos guardados en 'cases.json' y guarda los resultados para hacerle un analisis posterior
    """
    def __init__(self):
        super().__init__()
        self.questions = 0
        self.diagnostic = ""
        self.llm = FireworksProcessor(
            model_id=FIREWORKS_MODEL_ID,
            api_key=FIREWORKS_API_KEY,
            api_url=API_URL
        )
        
    def generar_respuesta_diagnostico(self, diagnostico, entidades):
        self.diagnostic = super().generar_respuesta_diagnostico(diagnostico, entidades)
    
    def generar_respuesta_error(self, mensaje):
        print (mensaje)
    
    def preguntar_usuario(self, question):
        self.confirmation = None
        if self.questions:
            self.questions -= 1
            self.confirmation = True
            return
        if self.questions == 0:
            return False  
    
    def run(self, case, questions = 3, output_csv = 'A_results.csv'):
        self.questions = questions
        # diagnosticar
        try: 
            time_init = time.time()
            query = case['consulta']
            self.orchestrator.diagnosticar(query)
            total_time = time.time() - time_init
        except Exception as e:
            print(e)
            return

        # comparar el diagnostico obtenido con el esperado usando LLM
        
        expected_answer = case["diagnostico_esperado"]
        
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
            f"Diagnóstico a evaluar: {self.diagnostic}\n"
            f"Respuesta (solo el entero 0 y 5): "
        )
        
        n=3
        while n:
            try:
                response = self.llm._llm_request(evaluator_prompt, temperature=0.8)
                break
            except:
                if n == 0:
                    return
                n-=1
                print("reintento en 10s ...")
                time.sleep(10)
                continue
        if n == 0:
            return
        
        score = int(response.split()[-1])
        
        print(self.diagnostic,'\n')
        print("Score: ", score)
        print('\n', '='*20 , '\n')
        
        
        #obtener la lista de los sintomas y enfermedades que extrajo el sistema
        # cleaner = self.orchestrator.cleaner
        # extractor = self.orchestrator.extractor
        # try:
        #     clean_query = cleaner(query)
        # except:
        #     clean_query = query
        
        # while True:
        #     try:    
        #         entities = extractor(clean_query)
        #         break
        #     except:
        #         continue
        
        # all_entities = list(set(self.orchestrator.flatten_dictionary(entities)))
        
        # # Guardar en CSV
        # fieldnames = [
        #     "consulta", "diagnostico_esperado", "diagnostico_generado",
        #     "puntuacion", "entidades_extraidas", "sintomas_reales", 
        #     "tiempo_total_seg", "cantidad_preguntas"
        # ]

        # try:
        #     with open(output_csv, "a", newline="", encoding="utf-8") as csvfile:
        #         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #         if csvfile.tell() == 0:
        #             writer.writeheader()
        #         writer.writerow({
        #             "consulta": query,
        #             "diagnostico_esperado": expected_answer,
        #             "diagnostico_generado": self.diagnostic,
        #             "puntuacion": score,
        #             "entidades_extraidas": ", ".join(all_entities),
        #             "sintomas_reales" : case["sintomas_reales"],
        #             "tiempo_total_seg": total_time,
        #             "cantidad_preguntas": questions
        #         })
        # except Exception as e:
        #     print(f"[Error] No se pudo escribir en el CSV: {e}")
        

with open("experiments/cases.json", "r", encoding="utf-8") as f:
    cases = json.load(f)

exp = ExpA()

for case in cases:
    # exp.run(case = case,questions = 3)      # questions es la cantidad de preguntas que hara como maximo el Sistema
    exp.run(case = case,questions = 2) 
    exp.run(case = case,questions = 1)      
    exp.run(case = case,questions = 0)
