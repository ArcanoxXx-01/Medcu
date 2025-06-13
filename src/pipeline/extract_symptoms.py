
def extract_symptoms(text: str) -> list:
    """Extrae síntomas/enfermedades desde texto clínico utilizando un LLM biomédico o NER.

    Args:
        text (str): texto al cualse le extraeran los sintomas, enfermedades, etc

    Returns:
        list[str]: lista con los sintomas, enfermedades, etc extraidos de 'text'
    """
    # TODO: Integrar con scispaCy, BioBERT o un LLM especializado
    sintomas = ["fiebre", "dolor de cabeza"]  # Ejemplo simulado
    return sintomas


def extract_new_symptoms(texts: list[str], symptoms: list[str]) -> list[str]:
    """ Extrae entidades biomédicas (sintomas, enfermedades, etc) de textos recuperados (base vectorial).
    Solo extrae los que son distintos a los que ya mencionó el usuario.

    Args:
        texts (list[str]): Lista con los textos recuperados de la base vectorial.
        symptoms (list[str]): Lista con los sintomas que meciono originalmente el ususario.

    Returns:
        list[str]: Lista con los nuevos sintomas extraidos de 'texts' y que no estan presentes en 'symptoms'
    """
    new_symptoms = []
    for text in texts:
        new_symptoms.extend([x for x in extract_symptoms(text) if x not in symptoms and x not in new_symptoms])
        
    return new_symptoms
