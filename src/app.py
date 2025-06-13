import streamlit as st
# from agents import neumologia_agent, cardiologia_agent

st.set_page_config(page_title="Diagnóstico Médico", layout="centered")

st.title("Sistema de Diagnóstico Médico")

# especialidad = st.selectbox("Selecciona una especialidad:", ["Neumología", "Cardiología"])

sintomas = st.text_area("Describe los síntomas del paciente:")

if st.button("Diagnosticar"):
    # if especialidad == "Neumología":
        # resultado = neumologia_agent.diagnosticar(sintomas)
    # elif especialidad == "Cardiología":
        # resultado = cardiologia_agent.diagnosticar(sintomas)
    resultado = {'enfermedad':"despingao" , 'confianza': 100}
    st.subheader("Resultado del Diagnóstico")
    st.write(f"**Enfermedad sugerida:** {resultado['enfermedad']}")
    st.write(f"**Confianza:** {resultado['confianza']}%")
