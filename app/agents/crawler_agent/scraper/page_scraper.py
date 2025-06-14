import requests
from bs4 import BeautifulSoup
from typing import Optional, Tuple

def scrape_article(url: str) -> Optional[Tuple[str, str]]:
    """
    Scrapea el contenido principal de un artículo de MedlinePlus.

    Args:
        url (str): URL del artículo a scrappear.

    Returns:
        Optional[Tuple[str, str]]: Tupla (título, contenido) si es válido, o None si es página por defecto.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Verificar si es página inválida (default)
    if soup.find("h1", string="Lo sentimos, pero no hemos podido encontrar la página que usted ha solicitado."):
        return None

    # Extraer título y contenido
    titulo_tag = soup.find("h1")
    content_div = soup.find("div", {"id": "d-article"})

    if not titulo_tag or not content_div:
        return None

    titulo = titulo_tag.get_text(strip=True)
    contenido = content_div.get_text(separator="\n", strip=True)
    return titulo, contenido
