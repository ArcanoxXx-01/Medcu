import streamlit as st

class Orchestrator:
    def __init__(self, 
                 cleaner, 
                 extractor, 
                 embedder, 
                 vector_store, 
                 knowledge_graph,
                 responder,
                 similarity_threshold=0.8,
                 top_k=5,
                 feedback_gain_threshold=1.0):
        self.cleaner = cleaner
        self.extractor = extractor
        self.embedder = embedder
        self.vector_store = vector_store
        self.knowledge_graph = knowledge_graph
        self.responder = responder
        self.similarity_threshold = similarity_threshold
        self.top_k = top_k
        self.feedback_gain_threshold = feedback_gain_threshold

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 4a9bfae (All pipeline)
    def diagnosticar(self, consulta_original: str):
        # print("comenzo a procesar la consulta")
        
=======
    def diagnosticar(self, query: str):
        print("Iniciando proceso de diagnóstico")

>>>>>>> 1416fff (only the GUI needs to be fixed)
        # Paso 1: Limpieza de texto
        try:
            clean_query = self.cleaner(query)
        except Exception:
<<<<<<< HEAD
            print("Fallo en [Modulo de Limpieza]: continuando con consulta original")
            consulta_limpia = consulta_original
<<<<<<< HEAD
=======
            print("Fallo en [Módulo de Limpieza]:\n continuando con consulta original")
            clean_query = query
>>>>>>> 1416fff (only the GUI needs to be fixed)

        # Paso 2: Extracción de entidades médicas
        try:
            print("Consulta limpiada correctamente")
            extracted_entities_as_dict = self.extractor(clean_query)
            print(f"Entidades médicas extraidas:\n  {extracted_entities_as_dict}\n")
            all_extracted_entities = list(set(self.flatten_dictionary(extracted_entities_as_dict)))
        except Exception as e:
            return self.responder.generar_respuesta_error(f"Fallo en [Módulo de extracción de entidades médicas]:\n {e}\n")

        # Paso 3: Embeddings
        try:
            if not all_extracted_entities:
                raise ValueError("No se encontraron sintomas ni enfermedades en la consulta\n")
            print("Obteniendo embeddings...")
            embeddings = self.embedder(all_extracted_entities)
        except ValueError as e:
            return self.responder.generar_respuesta_error(e)
        except Exception as e:
            print(f"Fallo en [Modulo de Generacion de Embeddings]:\n {e}\n Continuando con consulta sin ampliar...")
            embeddings = []
            
        # Paso 4
        related_chunks_results = []
        if embeddings:
            for embedding in embeddings:
                try:
                    related_chunks_results.extend(self.vector_store.search(embedding, top_k=self.top_k))
                except Exception as e:
                    print(f"Fallo al comparar embeddings:\n{e}\n\nBuscando información de internet para ampliar la consulta...\n")
                    # related_chunks_results = []  # Aquí iría el fallback al crawler

        # Paso 5: Recuperar entidades de chunks
        recovered_entities = []
        if related_chunks_results:
            try:
                for result_dict in related_chunks_results:
                    recovered_entities.extend(self.concat_values(result_dict))
                recovered_entities = (recovered_entities)
                # print("recover entities: ",recovered_entities)
            except Exception as e:
                print(f"Fallo al extraer información de los chunks recuperados:\n{e}\nContinuando sin dicha información...")
                
        # Paso 6: Inferencia inicial
        try:
            black_nodes = self.knowledge_graph.obtener_nodos_asociados(all_extracted_entities)
            # print("black nodes: ",black_nodes)
        except Exception as e:
            return self.responder.generar_respuesta_error(f"Fallo en la identificación de nodos en de la base de conocimientos:\n{e}\n")
        
        try:
            best_diagnostic = self.knowledge_graph.infer_diagnosis(black_nodes)
        except Exception:
            return self.responder.generar_respuesta_error(f"Fallo durante la diagnosticación: {e}")
            
        # Paso 7-10: Feedback iterativo
        try:
            gray_nodes = self.knowledge_graph.obtener_nodos_asociados(recovered_entities)
            # print ("gray nodes: ",gray_nodes)
            while True:
                print("Generando pregunta de feedback...")
                sugerencia = self.knowledge_graph.sugerir_pregunta_feedback(black_nodes, gray_nodes)
                if not sugerencia:
                    break
                user_confirm = self.responder.preguntar_usuario(sugerencia)
                print(user_confirm)
                if user_confirm:
                    black_nodes.append(sugerencia)
                    best_diagnostic = self.knowledge_graph.infer_diagnosis(black_nodes)
                    # Aqui seria procesar la entidad que se añadio a la consulta para añadir nuevos nodos grices
                else:
                    gray_nodes.remove(sugerencia)

                if best_diagnostic and best_diagnostic[0][1] >= self.feedback_gain_threshold:
                    break
        except Exception as e:
            print(f"Fallo durante la obtencion de feedback: \n{e} \ndevolver mejor diagnostico hasta el momento")
            
        try:
            return self.responder.generar_respuesta_diagnostico(best_diagnostic, all_extracted_entities) # <== poner los nodos negros en vez de all_entities
        
        except Exception as e:
            return self.responder.generar_respuesta_error(f"Fallo durante la generacion del diagnostico: {e}")
    
    def flatten_dictionary(dself, diccionario):
        resultado = []
        if diccionario:
            for valores in diccionario.values():
                resultado.extend(valores)
        return resultado
    
    def concat_values(dself, diccionario):
        resultado = []
        if diccionario:
            for valores in diccionario.values():
                if valores:
                    resultado.append(valores)
        return resultado

<<<<<<< HEAD
=======
class OrquestadorMedico:
    def __init__(self):
        self.diagnostic = "Perdón, aún no he sido capaz de generar un diagóstico."
        " Podrías volver a intentarlo explicando detalladamente los síntomas que presentas"
=======
>>>>>>> 4a9bfae (All pipeline)

        # Paso 2: Extracción de entidades médicas
        try:
            print("consulta limpiada")
            entidades = self.extractor(consulta_limpia)
            # print(entidades)
        except Exception as e:
            return self.responder.generar_respuesta_error(f"Fallo en el modulo de extraccion de entidades medicas: {e}")

        # Paso 3: Embeddings
        try:
            print("consulta procesada")
            input = self.concatenar_valores(entidades)
            if not input:
                self.responder.generar_respuesta_error("No se encontraron sintomas ni enfermedades en la consulta")
                raise ValueError("No se encontraron sintomas ni enfermedades en la consulta")
            embeddings = self.embedder([" ".join(input)])
        except ValueError as e:
            return self.responder.generar_respuesta_error(e)
        except Exception as e:
            print(f"Fallo en [Modulo de Generacion de Embeddings]: {e}\n continuando con consulta sin ampliar...")
            embeddings = []

        # Paso 4: Búsqueda en base vectorial
        print("consulta embeddingsada")
        chunks_relacionados = []
        if embeddings:
            try:
                for emb in embeddings:
                    resultados = self.vector_store.search(emb, top_k=self.top_k)
                    chunks_relacionados.extend(resultados)
            except Exception:
                print("Fallo al comparar embeddings: continuando sin recuperar informacion relacionada con el embedding")
                pass

        # Paso 5: Recuperar entidades de chunks
        try:
            print("Chunks recuperados")
            entidades_recuperadas = []
            for chunk in chunks_relacionados:
                new_entities = self.vector_store.get_by_chunk(chunk)
                if new_entities:
                    new_entities['url'] = []
                    new_entities['chunk_index'] = []
                    new_entities['text_chunk'] = []
                    new_entities['embedding'] = []
                    entidades_recuperadas.extend(self.concatenar_valores(new_entities))
            entidades_recuperadas = list(set(entidades_recuperadas))
            
        except Exception:
            print("Fallo al extraer informacion de los chunks recuperados: continuando sin dicha informacion")
            
        # Paso 6: Inferencia inicial
        print("consulta ampliada")
        try:
            nodos_negros = self.knowledge_graph.obtener_nodos_asociados(self.concatenar_valores(entidades))
        except Exception as e:
            return self.responder.generar_respuesta_error(f"Fallo en la identificacion de nodos en de la base de conocimientos: {e}")
        
        try:
            mejor_diag = self.knowledge_graph.infer_diagnosis(nodos_negros)
        except Exception:
            return self.responder.generar_respuesta_error(f"Fallo durante la diagnosticacion: {e}")
            
        # Paso 7-10: Feedback iterativo
        print("Pregunta para generar")
        try:
            nodos_grises = self.knowledge_graph.obtener_nodos_asociados(entidades_recuperadas)
            while True:
                sugerencia = self.knowledge_graph.sugerir_pregunta_feedback(nodos_negros, nodos_grises)
                if not sugerencia:
                    break

                quiere_confirmar = self.responder.preguntar_usuario(sugerencia)
                if quiere_confirmar:
                    nodos_negros.append(sugerencia)
                    mejor_diag = self.knowledge_graph.infer_diagnosis(nodos_negros)
                else:
                    nodos_grises.remove(sugerencia)

                if mejor_diag and mejor_diag[0][1] >= self.feedback_gain_threshold:
                    break
        except:
            print("Fallo durante la obtencion de feedback: devolver mejor diagnostico hasta el momento")
            
        try:
            return self.responder.generar_respuesta_diagnostico(mejor_diag)
        
        except Exception as e:
            return self.responder.generar_respuesta_error(f"Fallo durante la generacion del diagnostico: {e}")
            
    # def _extraer_entidades_de_chunks(self, chunks):
    #     entidades = set()
    #     for url, idx, texto, _ in chunks:
    #         # O usar extractor sobre los textos de los chunks
    #         try:
    #             extraidas = self.extractor.extraer(texto)
    #             entidades.update(extraidas)
    #         except Exception:
    #             continue
    #     return list(entidades)
    
<<<<<<< HEAD
>>>>>>> bf9eccf (Knowledge Graph)
=======
    def concatenar_valores(diccionario, a=None):
        resultado = []
        for valores in diccionario.values():
            resultado.extend(valores)
        return resultado

>>>>>>> 4a9bfae (All pipeline)
=======

>>>>>>> 1416fff (only the GUI needs to be fixed)
