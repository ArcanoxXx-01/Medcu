import streamlit as st
import traceback
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
    t_build_kb = threading.Thread(target=knowledge_graph.build_graph)
    t_build_kb.start()

    # csv_dir = "data/edges.csv"
    # try:
    #     knowledge_graph.add_edges_from_csv(csv_dir)
    # except Exception:
    #     print(f"No se pudieron agregar aristas desde: '{csv_dir}'")
    
    class ResponderStreamlit(ResponderInterface):
        def generar_respuesta_error(self, mensaje: str) -> None:
            st.error(f"⚠️ {mensaje}")

        def generar_respuesta_diagnostico(self, diagnostico: str, entidades: list[str]) -> None:
            st.markdown(process_model.generate_diagnostic(diagnostico, entidades))

        def preguntar_usuario(self, entidad: str) -> bool:
            question = process_model.generate_question(entidad)
            respuesta = st.radio(
                question,
                ["Sí", "No"],
                key=entidad
            )
            if respuesta == "Sí":
                return True
            return None

    orchestrator = Orchestrator(
        cleaner = process_model.limpiar_consulta,
        extractor = process_model.extraer_entidades,
        embedder = embeddings_model.embed_texts,
        vector_store = vec_store,
        knowledge_graph = knowledge_graph,
        responder = ResponderStreamlit(),
        similarity_threshold = 0.8,
        top_k = 5,
        feedback_gain_threshold = 1
    )
    
    crawler = Crawler()
    t_crawler = threading.Thread(target=crawler.run, daemon=True)
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
        
        # # Paso 1: limpiar consulta
        # texto_limpio = process_model.limpiar_consulta(consulta)
        # st.subheader("🧹 Consulta procesada:")
        # st.write(texto_limpio)

        # # Paso 2: extraer entidades médicas
        # entidades = process_model.extraer_entidades(texto_limpio)
        # sintomas = entidades.get("sintomas", [])
        # enfermedades = entidades.get("enfermedades", [])
        # st.subheader("🧠 Entidades médicas detectadas:")
        # st.write(f"Síntomas: {sintomas}")
        # st.write(f"Enfermedades: {enfermedades}")

        # # Paso 3: generar embedding
        # entradas = sintomas + enfermedades
        # if not entradas:
        #     st.warning("No se detectaron síntomas ni enfermedades para continuar.")
        #     return
        # embeddings = embedder.embed_texts([" ".join(entradas)])
        # st.write(embeddings)
        
        # Paso 4: recuperar información
        # documentos = retriever.retrieve(embeddings)
        # if not documentos:
        #     st.warning("⚠️ No se encontró información en la base vectorial. Buscando en internet...")
        #     documentos = buscar_en_internet(sintomas, enfermedades)

        # st.subheader("📄 Buscando Información relevante...")
        # for i, doc in enumerate(documentos, 1):
        #     st.markdown(f"**Doc {i}:** {doc.get('texto', '')[:300]}...")

        # # Paso 5: orquestador
        # especialidad = orquestador.inferir_especialidad(sintomas, enfermedades)
        # diagnostico = orquestador.diagnosticar(sintomas, enfermedades, documentos)

        # st.subheader("🏥 Especialidad inferida:")
        # st.write(especialidad)

        # st.subheader("✅ Diagnóstico preliminar:")
        # st.write(diagnostico)