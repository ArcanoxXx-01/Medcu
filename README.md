# MediCub

un asistente medico impulsado por IA.

autores:

-
-
-

link del proyecto:

-

Descripción del tema

El objetivo detras de Medicub era crear un sistema capaz de dar apoyo a los medico sdurante una consulta, o servir de preconsulta para un paciente.
Es decir un sistema capaz de recibir consultas en LN donde se explique la situacion del paciente (sintomas, enfermedades, etc) y genere un prediagnostico.
El objetivo de este sistema no es el de remplazar a un medico, sino ser un asistente medico.

- Explicación de la(s) solución(es) implementada(s):

La idea central de la implementacion se baso en simular el comportamiento de un medico durante una consulta. Con ayuda de expertos se definio que dicha simulacion se divide en las siguientes etapas:

1-El paciente explica su situacion, lo que le paso o los sintomas que posee.
2-El doctor analisa lo que le dice el paciente, y desde su conocimiento y experiencia busca que enfermedades podrian estar relacionadas con lo que le dijo el paciente (llamemos E1 a dicho conjunto de enfermedades).
3-Si aun no tiene la informacion suficiente para dar un diagnostico el doctor le preguntara al paciente si posee otros sintomas que esten relacionados con las enfermedades presentes en E1, para esto usa una estrategia de preguntar primero por los sintomas que acotan lo mas posible el espacio de las Enfermedades.
4-El doctor repite este proceso hasta tener un conjunto de enfermedades, las cuales son muy probables segun los sintomas del paciente.
5-Luego de esto el doctor seguiria los procedimientos para descartar o ratificar cada una de estas enfermeades, ya sea con pruebas, analisis u otros medios.
6-Luego de esto diagnostica segun los resultados del paso anterior.

Una vez entendidas las faces se definieron los componentes necesarios para que el sistema pudiera realizar dicha simulacion:

-Procesador de consulta: su objetivo es extraer la informacion importante de la consulta.
    -limpiar consulta.
    -extraer entidades medicas (enfermedades, sintomas).

-Expansor de consulta:
    -Busca en una base vectorial los fragmentos de textos que esten directamente relacionados con las entidades de la consulta.
    -




La idea central para la implementacion era crea un sistema multiagentes compuesto por los siguientes agentes:

-Crawler: se encargara de mantener actualizada la base de documentos y la base vectorial.
-Orquestador: como su nombre indica es el que orquesta al resto de modulos y agentes del sistema.
-Generador de preguntas: agente que se encargara de dado un conjunto de Entidades medicas (sintomas, enfermedades) utilisara su base de conocimientos para inferir que 