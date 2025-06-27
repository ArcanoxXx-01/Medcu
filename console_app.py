from app.agents.orchestrator.orchestrator import Orchestrator
from app.core.processor import FireworksProcessor
from app.core.embeddings import EmbeddingGenerator
from app.agents.crawler_agent.database.vector_store import VectorStore
from app.agents.crawler_agent.agent import Crawler
from app.agents.questioner.heuristic_selector import KnowledgeGraph, Heuristic_Selector
from app.config import *

class Asisstant():
    # Inicializar componentes
    def __init__(self):
        self.confirmation = None
        self.process_model = FireworksProcessor(
            model_id=FIREWORKS_MODEL_ID,
            api_key=FIREWORKS_API_KEY,
            api_url=API_URL
        )
        
        self.embeddings_model = EmbeddingGenerator(
            model_id = FIREWORKS_EMBEDDING_MODEL, 
            api_key = FIREWORKS_API_KEY, 
            url = EMBEDDING_URL
        )

        self.vec_store = VectorStore()
        self.knowledge_graph = KnowledgeGraph(use_db=True, use_csv=True)
        self.knowledge_graph.summary()
        self.selector = Heuristic_Selector(self.knowledge_graph)
            
        self.orchestrator = Orchestrator(
            processor = self.process_model,
            embedder = self.embeddings_model,
            vector_store = self.vec_store,
            selector = self.selector,
            responder = self,
            similarity_threshold = 0.8,
            top_k = 15,
            feedback_gain_threshold = 1
        )
               
    def generar_respuesta_error(self, mensaje: str):
        pass
    
    def generar_respuesta_diagnostico(self, diagnostico: str, entidades: list[str]):
        pass
                        
    def preguntar_usuario(self, question: str):
        pass
        
    def run(self):
        """Inicia una consulta"""
        pass
  
class Console_Assistant(Asisstant):
    def __init__(self):
        super().__init__()
               
    def generar_respuesta_error(self, mensaje: str) -> None:
        print(mensaje)#ponerle color o algo
    
    def generar_respuesta_diagnostico(self, diagnostico: str, entidades: list[str]) -> None:
        print("\nDiagnóstico:")
        try:
            print(self.process_model.generate_diagnostic(diagnostico, entidades))
        except:
            print("Fallo al crear la respuesta con LLM. \nUsando respuesta por defecto")
            print(f"Dado los síntomas descritos, es muy probable que presente '{diagnostico}', por favor consulte a un especialista")
    
    def preguntar_usuario(self, question: str) -> bool:
        print("\nConteste con 'Si' o 'No' a la pergunta siguiente:\n")
        print(question)
        
        response  = input().lower().strip()
                
        while response != "si" and response != "sí" and response != "no":
            print("Por favor, responda solo con 'si' o 'no'")
            response = input().lower().strip()
            
        self.confirmation = response != "no"
        
    def run(self):
        """Inicia una consulta
        """
        print('Medicub')
        print('🩺 Asistente Médico con IA\n')
        print('Describe tus síntomas o consulta médica:\n')

        consulta = ""
        
        while not consulta:
            consulta = input().strip()

        print("🔍 Procesando...")
        
        self.orchestrator.diagnosticar(consulta)

        print("\n\nPresione:\n X : para una nueva consulta\n Y : para repetir el diagnóstico\n Z : para finalizar")
        
        while True:
            option = input()
            if option == "x" or option == "X":
                self.run()
                return
            if option == "y" or option == "Y":
                self.orchestrator.diagnosticar(consulta)
                continue
            if option == "z" or option == "Z":
                #limpiar consola
                return
    
# app = Console_Assistant()
# app.run()