import os
from urllib.parse import urlparse
import re

def save_html_by_article_number(url: str, html_content: str, folder: str = "data/html_docs/"):
    """
    Guarda el contenido HTML en un archivo nombrado con el número de artículo extraído de la URL.

    Args:
        url (str): URL del artículo, p.ej. 'https://medlineplus.gov/spanish/ency/article/000123.htm'
        html_content (str): Contenido HTML a guardar.
        folder (str): Carpeta donde guardar el archivo (se crea si no existe).
    """
    # Crear carpeta si no existe
    os.makedirs(folder, exist_ok=True)

    # Extraer el número de artículo con regex
    # La URL termina en /article/XXXXXX.htm donde XXXXXX es el número de 6 dígitos
    match = re.search(r'/article/(\d{6})\.htm$', url)
    if not match:
        raise ValueError(f"No se pudo extraer número de artículo de la URL: {url}")
    
    article_number = match.group(1)

    # Ruta completa del archivo
    file_path = os.path.join(folder, f"{article_number}.html")

    # Guardar el contenido HTML
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Archivo guardado: {file_path}")
    
# save_html_by_article_number('https://medlineplus.gov/spanish/ency/article/000123.htm',"<div>Hola Mundo!!!</div>")
