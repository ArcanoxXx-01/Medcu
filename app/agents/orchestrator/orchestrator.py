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
=======
>>>>>>> 4a9bfae (All pipeline)
    def diagnosticar(self, consulta_original: str):
        # print("comenzo a procesar la consulta")
        
        # Paso 1: Limpieza de texto
        try:
            consulta_limpia = self.cleaner(consulta_original)
        except Exception:
            print("Fallo en [Modulo de Limpieza]: continuando con consulta original")
            consulta_limpia = consulta_original
<<<<<<< HEAD

        # Paso 2: Extracción de entidades médicas
        try:
            # print("consulta limpiada")
            entidades = self.extractor(consulta_limpia)
            # print(entidades)
        except Exception as e:
            return self.responder.generar_respuesta_error(f"Fallo en el modulo de extraccion de entidades medicas: {e}")

        # Paso 3: Embeddings
        try:
            # print("consulta procesada")
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
        # print("consulta embeddingsada")
        chunks_relacionados = []
        if embeddings:
            try:
                for emb in embeddings:
                    resultados = self.vector_store.search(emb, top_k=self.top_k)
                    chunks_relacionados.extend(resultados)
            except Exception:
                print("Fallo al comparar embeddings: continuando sin recuperar informacion relacionada con el embedding")
                pass
        print(chunks_relacionados)
        # Paso 5: Recuperar entidades de chunks
        try:
            # print("Chunks recuperados")
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
        # print("consulta ampliada")
        try:
            nodos_negros = self.knowledge_graph.obtener_nodos_asociados(self.concatenar_valores(entidades))
        except Exception as e:
            return self.responder.generar_respuesta_error(f"Fallo en la identificacion de nodos en de la base de conocimientos: {e}")
        
        try:
            mejor_diag = self.knowledge_graph.infer_diagnosis(nodos_negros)
        except Exception:
            return self.responder.generar_respuesta_error(f"Fallo durante la diagnosticacion: {e}")
            
        # Paso 7-10: Feedback iterativo
        # print("Pregunta para generar")
        try:
            nodos_grises = self.knowledge_graph.obtener_nodos_asociados(entidades_recuperadas)
            print(nodos_grises)
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
            return self.responder.generar_respuesta_diagnostico(mejor_diag, self.concatenar_valores(entidades))
        
        except Exception as e:
            return self.responder.generar_respuesta_error(f"Fallo durante la generacion del diagnostico: {e}")
            

    
    def concatenar_valores(dself, diccionario):
        resultado = []
        for valores in diccionario.values():
            resultado.extend(valores)
        return resultado

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
