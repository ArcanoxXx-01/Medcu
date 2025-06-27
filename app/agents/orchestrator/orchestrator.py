from app.core.processor import FireworksProcessor
from app.core.embeddings import EmbeddingGenerator
from app.agents.crawler_agent.database.vector_store import VectorStore
from app.agents.questioner.heuristic_selector import Heuristic_Selector

class Orchestrator:
    def __init__(self, 
                processor: FireworksProcessor,
                embedder: EmbeddingGenerator, 
                vector_store: VectorStore, 
                selector: Heuristic_Selector,
                responder,
                similarity_threshold:float =0.8,
                top_k: int =5,
                feedback_gain_threshold: float =5.0
                ):
        self.processor = processor
        self.embedder = embedder
        self.vector_store = vector_store
        self.selector = selector
        self.responder = responder
        self.similarity_threshold = similarity_threshold
        self.top_k = top_k
        self.feedback_gain_threshold = feedback_gain_threshold

    def diagnosticar(self, query: str):
        print("Iniciando proceso de diagnóstico...")

        # Paso 1: Limpieza de texto
        try:
            clean_query = self.processor.limpiar_consulta(query)
            print("[Módulo de Limpieza]: Consulta limpiada correctamente\n")
        except Exception as e:
            print(f"Fallo en [Módulo de Limpieza]:\n  {e}\ncontinuando con consulta original...\n")
            clean_query = query
            
        try:
            rows = self.processor.generate_edge(clean_query)
            self.selector.graph.save_in_csv(rows)
        except Exception as e:
            print("Error al agregar nuevo conocimiento al grafo:\n", e, '\n')

        # Paso 2: Extracción de entidades médicas
        try:
            extracted_entities_as_dict = self.processor.extraer_entidades(clean_query)
            print(f"[Módulo de extracción]: Entidades médicas extraidas\n")
            # print(extracted_entities_as_dict, '\n')
            all_extracted_entities = list(set(self.flatten_dictionary(extracted_entities_as_dict)))
        except Exception as e:
            return self.responder.generar_respuesta_error(f"Fallo en [Módulo de extracción de entidades médicas]:\n  {e}\n")

        # Paso 3: Embeddings
        try:
            if not all_extracted_entities:
                raise ValueError("No se encontraron sintomas ni enfermedades en la consulta\n")
            print("Obteniendo embeddings...")
            embeddings = self.embedder.embed_texts(all_extracted_entities)
        except ValueError as e:
            return self.responder.generar_respuesta_error(e)
        except Exception as e:
            print(f"Fallo en [Modulo de Generacion de Embeddings]:\n  {e}\n Continuando con consulta sin ampliar...")
            embeddings = []
            
        # Paso 4
        related_chunks_results = []
        if embeddings:
            print("[Módulo de nusqueda semántica]: Embeddings generados correctamente.\n")
            for embedding in embeddings:
                try:
                    related_chunks_results.extend(self.vector_store.search(embedding, top_k=self.top_k))
                except Exception as e:
                    print(f"[Módulo de nusqueda semántica]: Fallo al comparar embeddings:\n  {e}\n\nBuscando información de internet para ampliar la consulta...\n")
                    # related_chunks_results = []  # Aquí iría el fallback al crawler

        # Paso 5: Recuperar entidades de chunks
        recovered_entities = []
        if related_chunks_results:
            print("[Módulo de nusqueda semántica]: Inicando extracción de información de los chunks relevantes\n")
            try:
                for result_dict in related_chunks_results:
                    recovered_entities.extend(self.concat_values(result_dict))
                recovered_entities = list(set(recovered_entities))
                # print("recover entities: ",recovered_entities)
            except Exception as e:
                print(f"Fallo al extraer información de los chunks recuperados:\n  {e}\nContinuando sin dicha información...\n")
                
        # Paso 6: Inferencia inicial
        print("Iniciando búsqueda en el grafo de conocimientos\n")
        try:
            black_nodes = self.selector.graph.get_related_nodes(all_extracted_entities)
            # print("black nodes: ",black_nodes)
        except Exception as e:
            return self.responder.generar_respuesta_error(f"Fallo en la identificación de nodos en de la base de conocimientos:\n{e}\n")
        
        try:
            best_diagnostic = self.selector.infer_diagnostic(black_nodes)
        except Exception:
            return self.responder.generar_respuesta_error(f"Fallo durante la diagnosticación:  {e}")
               
        # Paso 7-10: Feedback iterativo
        try:
            gray_nodes = self.selector.graph.get_related_nodes(recovered_entities)
            
            while True:
                if not gray_nodes:
                    print("No hay mas preguntas :)")
                    break
                
                # print ("gray nodes: ",gray_nodes)
                
                print("Generando pregunta...")
                try:
                    sugerencia = self.selector.get(black_nodes, gray_nodes)
                except:
                    print("No se genero la pregunta")
                print("Entidad a preguntar: ", sugerencia)
                
                try:
                    question = self.processor.generate_question(sugerencia)
                except Exception as e:
                    question = f"¿Presenta el síntoma {sugerencia}?"
                    print(f"Fallo al generar la pregunta con LLM:\n  {e} \nUsando pregunta por defetco...")
                    
                self.responder.preguntar_usuario(question)
                
                while self.responder.confirmation is None:
                    continue
                                   
                if self.responder.confirmation:
                    black_nodes.extend(self.selector.graph.get_related_nodes([sugerencia]))
                    
                    best_diagnostic = self.selector.infer_diagnostic(black_nodes)
                    print(f"\nBuscando información sobre {sugerencia}")
                    try:
                        new_embedding = self.embedder.embed_texts([sugerencia])
                    except Exception as e:
                        print(f"Fallo al obtener nuva información:\n  {e}\n Continuando con información actual...")
                        new_embedding = []
                    
                    new_chunks = []
                    if new_embedding:
                        for embedding in new_embedding:
                            try:
                                new_chunks.extend(self.vector_store.search(embedding, top_k=self.top_k))
                            except Exception as e:
                                print(f"[Módulo de nusqueda semántica]: Fallo al comparar embeddings:\n  {e}\n\nBuscando información de internet para ampliar la consulta...\n")
                                # related_chunks_results = []  # Aquí iría el fallback al crawler

                    new_recovered_entities = []
                    if new_chunks:
                        try:
                            for result_dict in new_chunks:
                                new_recovered_entities.extend(self.concat_values(result_dict))
                            new_recovered_entities = list(set(recovered_entities))
                            # print("recover entities: ",recovered_entities)
                        except Exception as e:
                            print(f"Fallo al extraer las entidades de los chunks recuperados:\n{e}\nContinuando sin dicha información...")
                  
                    gray_nodes.extend(self.selector.graph.get_related_nodes(new_recovered_entities))
                else:
                    if gray_nodes.__contains__(sugerencia):
                        gray_nodes.remove(sugerencia)

                if best_diagnostic:
                    print("Beste diagnostic: ",best_diagnostic) 
                    if best_diagnostic[0][0] >= self.feedback_gain_threshold:
                        break
        except Exception as e:
            print(f"Fallo durante la obtencion de feedback: \n{e} \ndevolver mejor diagnostico hasta el momento")
            
        try:
            # print(best_diagnostic)
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
