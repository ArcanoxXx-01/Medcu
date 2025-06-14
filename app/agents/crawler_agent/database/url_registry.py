from datetime import datetime

def register_url(url: str, scrape_date: datetime):
    """
    Registra una URL como scrappeada, o actualiza la fecha si ya existe,
    para llevar control y evitar duplicados innecesarios.

    Parámetros:
    -----------
    url : str
        URL scrappeada.
    scrape_date : datetime
        Fecha y hora del scrappeo.
    """
    ...

def url_exists(url: str) -> bool:
    """
    Verifica si una URL ya está registrada en el sistema.

    Parámetros:
    -----------
    url : str
        URL a consultar.

    Retorna:
    --------
    bool
        True si la URL ya fue scrappeada, False en caso contrario.
    """
    ...
