from typing import Generator

def generate_medlineplus_urls(start_id: int = 0, end_id: int = 999999) -> Generator[str, None, None]:
    """
    Generador de URLs válidas de artículos médicos de MedlinePlus en español.

    Las URLs siguen el patrón:
    https://medlineplus.gov/spanish/ency/article/XXXXXX.htm
    donde XXXXXX es un número de 6 dígitos (con ceros a la izquierda si es necesario).

    Args:
        start_id (int): ID numérico inicial (por defecto: 0).
        end_id (int): ID numérico final (por defecto: 999999).

    Yields:
        str: URL generada correspondiente al artículo.

    Ejemplo:
        for url in generate_medlineplus_urls(100, 105):
            print(url)
            
        ### Output:
        ### https://medlineplus.gov/spanish/ency/article/000100.htm
        # ...
        ### https://medlineplus.gov/spanish/ency/article/000105.htm
    """
    base_url = "https://medlineplus.gov/spanish/ency/article/"

    for i in range(start_id, end_id + 1):
        article_id = f"{i:06d}"
        yield f"{base_url}{article_id}.htm"
