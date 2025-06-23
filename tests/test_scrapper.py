import requests
from bs4 import BeautifulSoup
import re
import json

def scrape(url):
  response = requests.get(url)
  response.raise_for_status()
  html = response.text

  soup = BeautifulSoup(html, 'lxml')

  h2 = soup.find('h2', class_='es-heading-h2', string=re.compile(r'Planteamiento:*'))

  if h2:
    nxt = h2.find_next_sibling(lambda tag: tag.name in ['p', 'div'])
    statement = nxt.get_text(strip=True) if nxt else None
  else:
    statement = None
  
  diagnostic_div = soup.find('div', class_='flr pr2')
  if diagnostic_div:
    tag_span = diagnostic_div.find('span', class_='es-tag tag-color small es-js-tooltip')
    if tag_span:
        inner = tag_span.find('span')
        diagnostic = inner.get_text(strip=True) if inner else tag_span.get_text(strip=True)
  else:
      diagnostic = None

  if (statement is None) or (diagnostic is None):
    return None
  
  return {'Consulta': statement, 'Diagnóstico': diagnostic}

base_url = 'https://www.fisterra.com/formacion/casos-clinicos/caso.asp?idCaso='

result = {}
for i in range(200, 340):
  cur = scrape(base_url + str(i))
  if cur is None: continue
  result[i] = cur

with open('tests.json', 'w', encoding='utf-8') as f:
  json.dump(result, f, ensure_ascii=False, indent=2)
