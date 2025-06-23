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
            
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
            'titulo', 'causas', 'sintomas', 'primeros_auxilios', 'no_se_debe', 'ejemplo_comsulta', 'nombres_alternativos'.
=======
            'titulo', 'causas', 'sintomas', 'primeros_auxilios', 'no_se_debe', ejemplo_comsulta, 'nombres_alternativos'.
>>>>>>> ef49f87 (add ejemplo_comsulta param to document db)
=======
            'titulo', 'causas', 'sintomas', 'primeros_auxilios', 'no_se_debe', 'ejemplo_comsulta', 'nombres_alternativos'.
>>>>>>> 9e4a382 (Bug fixes in the Crawler)
=======
            'enfermedad', 'causas', 'sintomas', 'nombres_alternativos'.
>>>>>>> 1416fff (only the GUI needs to be fixed)
            
            * Los valores serán cadenas vacías si no se encuentran las secciones.
    """
    content = correct_text(html_content)
    result = {
        'causas': '',
        'sintomas': '',
        'nombres_alternativos': ''
    }

    try:
        soup = BeautifulSoup(content, 'html.parser')

        enfermedad = soup.find('h1').get_text(strip=True)

        for section in soup.find_all('div', class_='section'):
            header = section.find(['h2', 'h3'])
            if not header:
                continue
            tittle = header.get_text(strip=True).lower()

            if 'causa' in tittle:
                result['causas'] = section.get_text(separator=' ', strip=True)
            elif 'síntoma' in tittle or 'sintoma' in tittle:
                result['sintomas'] = section.get_text(separator=' ', strip=True)
            elif 'nombres alternativos' in tittle:
                result['nombres_alternativos'] = section.get_text(separator=' ', strip=True)

<<<<<<< HEAD
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
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 9e4a382 (Bug fixes in the Crawler)
                
            elif section_name == 'Lo que se puede esperar en el consultorio médico':
                result['ejemplo_comsulta'] = correct_text(content)
                
<<<<<<< HEAD
=======
            elif section_name == 'Lo que se puede esperar en el consultorio médico':
                result['ejemplo_comsulta'] = correct_text(content)
>>>>>>> ef49f87 (add ejemplo_comsulta param to document db)
=======
>>>>>>> 9e4a382 (Bug fixes in the Crawler)
            elif section_name == 'Nombres alternativos':
                result['nombres_alternativos'] = correct_text(content)
=======
        return {
            'enfermedad': enfermedad,
            **result
        }
>>>>>>> 1416fff (only the GUI needs to be fixed)

    except Exception as e:
        print("Error al parsear el HTML: ", e)
        return None


def correct_text(text: str):
    text = text.replace("Ã¡", "á")
    text = text.replace("Ã©", "é")
    text = text.replace("Ã³", "ó")
    text = text.replace("Ã±", "ñ")
    text = text.replace("Ã­", "í")
    text = text.replace("Ãº", "ú")
    text.replace('\'','')
    text.replace('"','')
    return text.lower().strip()
    

# path = 'data/html_docs/000001.html'

# with open(path,'r')as f:
#     content = correct_text(f.read())
#     x = extract_relevant_sections(content)
#     print('Enfermedad:', x['enfermedad'],'\n')
#     print('Causas:',x['causas'],'\n')
#     print('Sintomas:',x['sintomas'],'\n')
#     print('Nombres Alternativos:',x['nombres_alternativos'],'\n')