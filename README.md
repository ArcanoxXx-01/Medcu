# MediCub, _un asistente médico impulsado por_ IA

Autores:

- Darío López Falcón
- Eduardo Brito Labrada
- Ernesto Abreus Peraza

Facultad de Matematica y Computacion ([MATCOM](https://matcom.uh.com.cu/)), de la Universidad de La Habana, Cuba

[link del proyecto](https://github.com/ArcanoxXx-01/MediCub/)

## Descripción del tema

El objetivo detras de **Medicub** era crear un sistema capaz de dar ***apoyo*** a los medicos durante una consulta, o servir de ***preconsulta*** para un paciente.
Es decir un sistema capaz de recibir consultas en Lenguaje Natural donde se explique la situacion del paciente ( _sintomas, enfermedades, ... ) y genere un prediagnostico.

***El objetivo de este sistema no es el de remplazar a un medico, sino ser un asistente medico.***

## Explicación de la solución implementada

La idea central de la implementacion se baso en simular el comportamiento de un medico durante una consulta.
Con ayuda de expertos se definio que dicha simulacion se divide en las siguientes etapas:

- **Explicacion del Paciente:**

El paciente explica su situacion, lo que le paso o los sintomas que posee, etc.

**Ejemplo:**

---

- **Extraccion de entidades medicas:**

El doctor extrae, e infiere entidades medicas de la explicacion que dio el usuario.

**Ejemplo:**

---

- **Descarte por conocimiento:**

El doctor analisa lo que le dice el paciente, y desde su conocimiento y experiencia busca que enfermedades podrian estar relacionadas con lo que le dijo el paciente

**Ejemplo:**

( *llamemos E1 a dicho conjunto de enfermedades* )

---

- **Retroalimentacion:**

Si aun no tiene la informacion suficiente para dar un diagnostico el doctor le preguntara al paciente si posee otros sintomas que esten relacionados con las enfermedades presentes en E1.

**Ejemplo:**

( *para esto usa una estrategia de preguntar primero por los sintomas que acotan lo mas posible el espacio de las Enfermedades.* )

---

- **Iterar:**

El doctor repite este proceso hasta tener un conjunto de enfermedades, las cuales son muy probables segun los sintomas del paciente.

---

- **Descartes por pruebas:**

Luego de esto el doctor seguiria los procedimientos para descartar o ratificar cada una de estas enfermeades, ya sea con pruebas, analisis u otros medios.

**Ejemplo:**

---

- **Diagnostico:**

Luego de esto diagnostica segun los resultados del paso anterior.

---

### Componentes principales:

Una vez entendidas las faces se definieron los componentes necesarios para que el sistema pudiera realizar dicha simulacion:

- **Procesador de consulta:** su objetivo es extraer la informacion importante de la consulta ( entidades medicas ):
  - limpiar consulta.
  - extraer entidades medicas (enfermedades, sintomas).

- **Expansor de consulta:** Este componente es de gran ayuda, ya que es el encardgado de cumplir con las faces 2, 3 y 4. Esta compuesto por:
  - Base metadatos asociados a vectors indexados.
  - Vectores Indexados
  - Generador de Ranking
  - Generador de Preguntas
  - Retroalimentacion

- **Crawler:** Agente cuyo objetivo es mantener actualizada en todo momento la base de dacomentos con la ultima informacion de la [enciclopedia medica de MediLinePlus en español](https://medlineplus.gov/spanish/ency/article/)

  - Scraper de articulos: obtiene el codigo `HTML` de los articulos de la enciclopedia que aun no estan en la base de documentos, o la ultima vez que se descargo fue hace mucho tiempo.
  - Extractor de informacion: procesa cada uno de los codigos `HTML` de los articulos previamente descargados, y les extrae la mayor cantidad de informacion posible, por ejemplo:
  
    - Causas, sintomas, nombres alternativos, procedimientos, contraindicaciones, ejemplo de consulta.
  - Chunker: Se encarga de tomar la informacion de cada articulo y generar un conjunto de chunks, cada uno acomañado de metadata.
  - Modelo de embedding: Se usa para generar los vectores de embedding de cada uno de los chunks, en nuestro caso por cuestiones de recursos usamos un [modelo gratuito de Fireworks.ai](https://api.fireworks.ai/inference/v1/embeddings/nomic-ai/nomic-embed-text-v1.5)

