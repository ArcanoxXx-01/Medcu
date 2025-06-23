
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
    "- Diagnóstico: {diagnostico}\n"
    "- Entidades médicas consideradas: {entidades}  # lista como síntomas, causas y enfermedades\n\n"
    "Instrucciones:\n"
    "1. Explica al usuario que, según los síntomas que ha reportado, el diagnóstico es {diagnostico}.\n"
    "2. Menciona las principales entidades médicas consideradas, agrupándolas si es posible (ej: síntomas observados, causas asociadas, enfermedades relacionadas).\n"
    "3. No des órdenes ni afirmes el diagnóstico como definitivo. Usa expresiones como \"es probable que...\", \"según los datos aportados...\", \"esto podría indicar...\".\n"
    "4. Si es apropiado, sugiere acudir a un profesional para confirmación.\n\n"
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

GENERATE_EDGE = (
"Extrae de forma estructurada las enfermedades, sus síntomas, sus causas y un peso que indique qué tan representativo es cada síntoma para esa enfermedad.\n"
"Devuelve la respuesta únicamente en formato CSV, con las siguientes columnas:\n"
"nombre,sintoma,causa,peso\n\n"
"    nombre: nombre de la enfermedad.\n"
"    sintoma: un síntoma asociado a la enfermedad (una por fila).\n"
"    causa: una posible causa de la enfermedad (una por fila).\n"
"    peso: número entre 0.0 y 1.0 que representa cuánto influye ese síntoma en la enfermedad (1.0 = síntoma característico).\n"
"No incluyas ningún comentario, explicación o texto adicional fuera del CSV.\n"
"Texto a analizar:\n"
"{query}\n"
"Ejemplo de salida esperada:\n"
"nombre,sintoma,causa,peso\n"
"enfermedad1,sintoma1,causa1,peso1\n"
"enfermedad2,sintoma2,causa2,peso2\n"
"Asegúrate de devolver en el formato correcto (incluya las comas y saltos de línes necesarios)"
)