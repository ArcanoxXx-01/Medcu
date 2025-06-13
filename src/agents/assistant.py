from pipeline import preprocess_query, extract_symptoms, embedding, vector_search, generate_questions
from agents import orchestator


def diagnose(user_query: str, structured_user_data: dict) -> dict:
    """Realiza todo el proceso necesario para generar un diagnostico para el usuario

    Args:
    
        user_query (str): Consulta en lenguaje natural
        structured_user_data (dict): Datos estructurados del usuario, ej:
        {
            DNI: 1234567890
            edad: 21
            genero: masculino
            enfermedades: -
            alergias: -
            ...
        }

    Returns:
        dict: Diccionario con metadatos para darle una respuesta al usuario, contiene los campos, ej:         
        {
            text: "Según la información que me diste es probable que presentes dengue",
            certainty: 89%,
            symptom: ['fiebre', 'dolor de cabeza', 'dolor en las articulaciones'],
            specialists: medicina interna
        }
    """
    try:
        # 1. Limpieza del texto
        try:
            descripcion_limpia = preprocess_query.preprocess(user_query)
        except(Exception)as e:
            raise(f"Error al limpiar la query original: {e}")

        # 2. Extracción de síntomas y enfermedades iniciales
        try:
            initials_symptoms = extract_symptoms.extract_symptoms(descripcion_limpia)
        except(Exception)as e:
            raise(f"Error al extraer los sintomas de la consulta original: {e}")

        # 3. Pasar los sintomas extraidos de la consulta por un modelo de embeddings 
        try:
            consult_vector = embedding.process(initials_symptoms)
        except(Exception)as e:
            raise(f"Error al pasar los sintomas extraindos por el modelo de embeddings: {e}")
        
        # 4. Recuperación semántica
        try:
            documentos_relacionados = vector_search.search_documents(consult_vector)
        except(Exception)as e:
            raise(f"Error al recuperar documentos relacionados con la consulta original: {e}")

        # 5. Enriquecer síntomas desde textos recuperados
        try:
            new_syptoms = extract_symptoms.extract_new_symptoms(documentos_relacionados, initials_symptoms)
        except(Exception)as e:
            raise(f"Error al extraer sintomas de los documentos recuperados: {e}")
        
        # 6. Generar preguntas para hacerle al usuario
        try:
            questions = generate_questions.generate_questions(new_syptoms)
        except(Exception)as e:
            raise(f"Error al generar las preguntas que se le haran al usuario: {e}")
        
        # 7. Hacerle las preguntas al usuario.
        try:
            new_user_information = []  # <======== despues ponerlo mas bonito con compresion de listas, lo dejo asi para que no marque errores
            if questions:
                for quest in questions:
                    new_user_information.append()  # <======== Preguntarle al usuario
        except(Exception)as e:
            raise(f"Error al hacerle las preguntas al usuario: {e}")
        
        # 8. Procesar la nueva informacion del usuario y extraer los sintomas, enfermedade, etc
        try:
            new_information_preprocess = preprocess_query.preprocess(new_user_information)
            new_syptoms = extract_symptoms.extract_symptoms(new_information_preprocess)
        except(Exception)as e:
            raise(f"Error al procesar las respuestas del usuario a las preguntas que se le hizo: {e}")
        
        # 9. Pasarle los sintomas al orquestador para que se encargue del diagnostico y devolver su resultado
        try:
            return orchestator.diagnose(initials_symptoms, new_syptoms)
        except(Exception)as e:
            raise(f"Error del Orquestador al diagnosticar: {e}")
    
    except(Exception) as e:
        print(e)
