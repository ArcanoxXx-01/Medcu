
def search_documents(sintomas: list[str]) -> list[str]:
    """Busca en la base vectorial textos relevantes relacionados con los síntomas.

    Args:
        sintomas (list[str]): lista de sintomas estrs=aidos de la consulta del usuario

    Returns:
        list[str]: lista con los documentos que superan el humbral de relevancia con respecto a los sintomas
    """
    # TODO: Implementar búsqueda con FAISS, ChromaDB o similar
    documentos = [
        "Los síntomas más comunes del dengue son fiebre, dolor detrás de los ojos y dolor en las articulaciones."
    ]
    return documentos