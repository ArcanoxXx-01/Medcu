
LIMPIAR_CONSULTA = (
    "Eres un asistente médico. Limpia el siguiente texto, eliminando palabras irrelevantes, "
    "errores gramaticales, muletillas o repeticiones, pero manteniendo el significado original. "
    "Solo devuelve el texto limpio.\n\nConsulta: {consulta}\n\nTexto limpio:"
)

EXTRAER_ENTIDADES = (
    "Extrae los síntomas y enfermedades mencionados en el siguiente texto médico. "
    "Devuélvelo en formato JSON con dos claves: 'sintomas' y 'enfermedades', donde cada clave contiene una lista.\n\n"
    "Importante: solo devuelve el JSON y no devuelvas texto explicando el por que de tu respuesta"
    "Texto: {texto}\n\nEjemplo de salida:\n"
    "{{\n  \"sintomas\": [\"tos\", \"fiebre\"],\n  \"enfermedades\": [\"asma\"]\n}}\n\nRespuesta:"
)
