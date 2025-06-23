import streamlit as st
import threading

from app.agents.orchestrator.orchestrator import Orchestrator
from app.core.processor import FireworksProcessor
from app.core.embeddings import EmbeddingGenerator
from app.core.responder import ResponderInterface
from app.agents.crawler_agent.database.doc_store import DocumentStore
from app.agents.crawler_agent.database.vector_store import VectorStore
from app.agents.crawler_agent.agent import Crawler
from app.agents.diagnostician.graph import MedicalGraphBuilder
from app.config import *


def main():
    
    # Inicializar componentes
    process_model = FireworksProcessor(
        model_id=FIREWORKS_MODEL_ID,
        api_key=FIREWORKS_API_KEY,
        api_url=API_URL
    )

    embeddings_model = EmbeddingGenerator(
        model_id = FIREWORKS_EMBEDDING_MODEL, 
        api_key = FIREWORKS_API_KEY, 
        url = EMBEDDING_URL
    )

    vec_store = VectorStore()

    knowledge_graph = MedicalGraphBuilder()
    
    # t_build_kb = threading.Thread(target=knowledge_graph.build_graph())
    # t_build_kb.start()

    # csv_dir = "data/edges.csv"
    # try:
    #     knowledge_graph.add_edges_from_csv(csv_dir)
    # except Exception:
    #     print(f"No se pudieron agregar aristas desde: '{csv_dir}'")
    
    class ResponderStreamlit(ResponderInterface):
        def __init__(self):
            super().__init__()
            self.confirmation = None
            
        def generar_respuesta_error(self, mensaje: str) -> None:
            st.error(f"⚠️ {mensaje}")

        def generar_respuesta_diagnostico(self, diagnostico: str, entidades: list[str]) -> None:
            try:
                st.markdown(process_model.generate_diagnostic(diagnostico, entidades))
            except:
                st.markdown(f"Dado los síntomas descritos, es muy probable que presente '{diagnostico}', por favor consulte a un especialista")
                print("Fallo al crear la respuesta con LLM. \nUsando respuesta por defecto")
                
        def preguntar_usuario(self, question: str) -> bool:
                
            seleccion = st.radio(question, ["Seleccione una opción:", "Sí", "No"])

            if seleccion is not None:
                self.confirmation = seleccion == "Sí"
            
            st.stop()
                

    orchestrator = Orchestrator(
        cleaner = process_model.limpiar_consulta,
        extractor = process_model.extraer_entidades,
        embedder = embeddings_model.embed_texts,
        questioner = process_model.generate_question,
        vector_store = vec_store,
        knowledge_graph = knowledge_graph,
        responder = ResponderStreamlit(),
        similarity_threshold = 0.8,
        top_k = 15,
        feedback_gain_threshold = 1
    )
    
    # crawler = Crawler()
    # t_crawler = threading.Thread(target=crawler.run, daemon=True)
    # t_crawler.start()
    
    # Compoenentes de la UI
    st.set_page_config(page_title='Medicub')
    st.title('🩺 Asistente Médico con IA')

    consulta = st.text_area('Describe tus síntomas o consulta médica:', height=150)

    if st.button('Enviar'):
        if not consulta.strip():
            st.warning('Por favor, escribe una consulta.')
            return

        st.info('🔍 Procesando...')
        response = orchestrator.diagnosticar(consulta)
        st.write(response)
