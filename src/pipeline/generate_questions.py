
def generate_questions(extracted_symptoms: list[str]) -> list[str]:
    """Genera preguntas aclaratorias sobre síntomas no mencionados por el usuario.

    Args:
        extracted_symptoms (list[str]): [description]

    Returns:
        list[str]: lista con las preguntas formuladas,listas para enviarselas al usuario
    """
    preguntas = []
    for sintoma in extracted_symptoms:
        preguntas.append(f"¿Presenta {sintoma}?") #Despues lo podemos cambiar por un LLM para que sea algo mas coherente
    return preguntas