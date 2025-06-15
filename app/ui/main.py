import streamlit as st
from app.core.processor import FireworksProcessor
from app.core.embeddings import EmbeddingGenerator
from app.core.retrieval import VectorRetriever
# from orchestrator.orchestrator import OrquestadorMedico
from app.agents.crawler_agent.agent import Crawler
from app.config import *

def main():
    # Inicializar componentes
    processor = FireworksProcessor(FIREWORKS_MODEL_ID, FIREWORKS_API_KEY, API_URL)
    embedder = EmbeddingGenerator("fireworks", FIREWORKS_EMBEDDING_MODEL, FIREWORKS_API_KEY, EMBEDDING_URL)
    retriever = VectorRetriever()
    # orquestador = OrquestadorMedico()
    # crawler = Crawler()
    # crawler.run()
    
    # Compoenentes de la UI
    st.set_page_config(page_title='Medicub')
    st.title('🩺 Asistente Médico con IA')

    consulta = st.text_area('Describe tus síntomas o consulta médica:', height=150)

    if st.button('Enviar'):
        if not consulta.strip():
            st.warning('Por favor, escribe una consulta.')
            return

        st.info('🔍 Procesando...')

        # Paso 1: limpiar consulta
        texto_limpio = processor.limpiar_consulta(consulta)
        st.subheader("🧹 Consulta procesada:")
        st.write(texto_limpio)

        # Paso 2: extraer entidades médicas
        entidades = processor.extraer_entidades(texto_limpio)
        sintomas = entidades.get("sintomas", [])
        enfermedades = entidades.get("enfermedades", [])
        st.subheader("🧠 Entidades médicas detectadas:")
        st.write(f"Síntomas: {sintomas}")
        st.write(f"Enfermedades: {enfermedades}")

        # Paso 3: generar embedding
        entradas = sintomas + enfermedades
        if not entradas:
            st.warning("No se detectaron síntomas ni enfermedades para continuar.")
            return
        embeddings = embedder.embed_texts([" ".join(entradas)])
        st.write(embeddings)
        
    #     # # Paso 4: recuperar información
    #     # documentos = retriever.retrieve(embeddings)
    #     # if not documentos:
    #     #     st.warning("⚠️ No se encontró información en la base vectorial. Buscando en internet...")
    #     #     # documentos = buscar_en_internet(sintomas, enfermedades)

    #     # st.subheader("📄 Documentos relevantes:")
    #     # for i, doc in enumerate(documentos, 1):
    #     #     st.markdown(f"**Doc {i}:** {doc.get('texto', '')[:300]}...")

    #     # # Paso 5: orquestador
    #     # especialidad = orquestador.inferir_especialidad(sintomas, enfermedades)
    #     # diagnostico = orquestador.diagnosticar(sintomas, enfermedades, documentos)

    #     # st.subheader("🏥 Especialidad inferida:")
    #     # st.write(especialidad)

    #     # st.subheader("✅ Diagnóstico preliminar:")
    #     # st.write(diagnostico)
