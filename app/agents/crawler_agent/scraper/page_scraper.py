import requests
from bs4 import BeautifulSoup
from typing import Optional, Tuple

def scrape_article(url: str) -> Optional[Tuple[str, str]]:
    """
    Scrapea el contenido principal de un artículo de MedlinePlus.

    Args:
        url (str): URL del artículo a scrappear.

    Returns:
        str: Código HTML si es un artículo válido, o None si es página por defecto.
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        # ver que la pagina contenga un articulo
        if soup.find("h1", string="Lo sentimos, pero no hemos podido encontrar la página que usted ha solicitado."):
            return None
        return response.text
    
    except(Exception) as e:
        print(f"Error al scrapear la url {url}: {e}")
        return None
