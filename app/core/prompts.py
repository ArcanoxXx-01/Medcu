
LIMPIAR_CONSULTA = (
    "Eres un asistente médico. Limpia el siguiente texto, eliminando palabras irrelevantes, "
    "errores gramaticales, muletillas o repeticiones, pero manteniendo el significado original. "
    "Solo devuelve el texto limpio.\n\nConsulta: {consulta}\n\nTexto limpio:"
)

EXTRAER_ENTIDADES = (
    "Extrae los síntomas y enfermedades mencionados en el siguiente texto médico.\n"
    "Infiere los síntomas en caso de ser necesario.\n"
    "Devuélvelo en formato JSON con dos claves: 'sintomas' y 'enfermedades', donde cada clave contiene una lista.\n\n"
    "Importante: solo devuelve el JSON y no devuelvas texto explicando el por que de tu respuesta"
    "Texto: {texto}\n\nEjemplo de salida:\n"
    "{{\n  \"sintomas\": [\"tos\", \"fiebre\"],\n  \"enfermedades\": [\"asma\"]\n}}\n\nRespuesta:"
)

GENERATE_DIAGNOSTIC = (
    "Eres un asistente médico especializado en comunicar diagnósticos de manera clara y empática a pacientes no expertos. "
    "Tu tarea es redactar una respuesta natural y profesional que explique el posible diagnóstico y mencione brevemente los síntomas o causas en que se basa.\n\n"
    "Contexto:\n"
    "- Diagnóstico más probable: {diagnostico}\n"
    "- Entidades médicas consideradas: {entidades}  # lista como síntomas, causas y enfermedades\n\n"
    "Instrucciones:\n"
    "1. Explica al usuario que, según los síntomas que ha reportado, el diagnóstico más probable es {diagnostico}.\n"
    "2. Menciona las principales entidades médicas consideradas, agrupándolas si es posible (ej: síntomas observados, causas asociadas, enfermedades relacionadas).\n"
    "3. Usa un tono empático, claro y moderadamente técnico (sin jerga compleja).\n"
    "4. No des órdenes ni afirmes el diagnóstico como definitivo. Usa expresiones como \"es probable que...\", \"según los datos aportados...\", \"esto podría indicar...\".\n"
    "5. Si es apropiado, sugiere acudir a un profesional para confirmación.\n\n"
    "Devuelve únicamente el mensaje para el paciente. No incluyas encabezados ni notas fuera del cuerpo del texto."
)

GENERATE_QUESTION = (
    "Eres un asistente médico encargado de interactuar con pacientes no expertos. "
    "Tu tarea es generar una pregunta clara, amable y directa para saber si el paciente presenta o ha experimentado la siguiente entidad médica: \"{entidad}\".\n"
    "Instrucciones:\n"
    "1. Formula la pregunta en un lenguaje sencillo y comprensible para cualquier paciente.\n"
    "2. Evita términos médicos técnicos si no son necesarios, o explícalos brevemente.\n"
    "3. Mantén un tono empático y profesional.\n"
    "4. No hagas diagnósticos ni afirmaciones, solo realiza una pregunta sobre la presencia o ausencia de la entidad.\n"
    "Devuelve únicamente la pregunta final, sin encabezados ni notas adicionales."
)


PROCESAR_ENTIDADES = (
    "Eres un asistente médico especializado en extracción estructurada de información clínica. "
    "Tu tarea consiste en analizar descripciones textuales sobre una enfermedad y transformar su contenido en listas organizadas. "
    "Extrae todos los elementos relevantes de cada campo, separando conceptos distintos aunque estén unidos por conjunciones o puntuación.\n\n"
    "Entrada:\n"
    "- Enfermedad: {enfermedad}\n"
    "- Causas: {causas}\n"
    "- Síntomas: {sintomas}\n"
    "- Nombres alternativos: {nombres_alternativos}\n\n"
    "Salida esperada:\n"
    "Un diccionario en formato JSON con la siguiente estructura:\n"
    "{{\n"
    '  "enfermedad": "nombre de la enfermedad",\n'
    '  "causas": ["causa 1", "causa 2", "..."],\n'
    '  "sintomas": ["síntoma 1", "síntoma 2", "..."],\n'
    '  "nombres_alternativos": ["nombre 1", "nombre 2", "..."]\n'
    "}}\n\n"
    "Reglas:\n"
    "- No inventes información adicional.\n"
    "- No dejes listas vacías, usa `[]` si no hay información.\n"
    "- No expliques nada, responde solo con el JSON."
)
