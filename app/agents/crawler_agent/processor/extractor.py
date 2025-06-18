from bs4 import BeautifulSoup
from typing import Dict

def extract_relevant_sections(html_content: str) -> Dict[str, str]:
    """
    Procesa el HTML crudo para extraer las secciones médicas relevantes.

    Args:
        html_content (str): Código HTML completo de la página (sin procesar).

    ## Returns:
    
        Dict[str, str]:   
            Diccionario con la información extraída. Claves posibles:
            
            'titulo', 'causas', 'sintomas', 'primeros_auxilios', 'no_se_debe', 'ejemplo_comsulta', 'nombres_alternativos'.
            
            * Los valores serán cadenas vacías si no se encuentran las secciones.
    """
    result = {
        'titulo': '',
        'causas': '',
        'sintomas': '',
        'primeros_auxilios': '',
        'no_se_debe': '',
        'ejemplo_comsulta': '',
        'nombres_alternativos': ''
    }

    try:
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extraer título
        title_tag = soup.find('h1', class_='with-also')
        if title_tag:
            result['titulo'] = correct_text(title_tag.get_text(strip=True))

        # Extraer secciones
        sections = soup.find_all('div', class_='section')

        for section in sections:
            header = section.find('div', class_='section-header')
            if not header:
                continue

            section_title = header.find('h2')
            if not section_title:
                continue

            section_name = section_title.get_text(strip=True)
            section_body = section.find('div', class_='section-body')
            if not section_body:
                continue

            content = section_body.get_text('\n', strip=True)

            if section_name == 'Causas':
                result['causas'] = correct_text(content)
                
            elif section_name == 'Síntomas':
                result['sintomas'] = correct_text(content)
                
            elif section_name == 'Primeros auxilios':
                result['primeros_auxilios'] = correct_text(content)
                
            elif section_name == 'No se debe':
                result['no_se_debe'] = correct_text(content)
                
            elif section_name == 'Lo que se puede esperar en el consultorio médico':
                result['ejemplo_comsulta'] = correct_text(content)
                
            elif section_name == 'Nombres alternativos':
                result['nombres_alternativos'] = correct_text(content)

    except Exception as e:
        print("Error al parsear el HTML: ", e)
        return None

    return result

def correct_text(text: str):
    text = text.replace("Ã¡", "á")
    text = text.replace("Ã©", "é")
    text = text.replace("Ã³", "ó")
    text = text.replace("Ã±", "ñ")
    text = text.replace("Ã­", "í")
    text = text.replace("Ãº", "ú")
    return text
