from mimetypes import init
import threading, queue, time, os
from typing import Dict, List

from .database.doc_store import DocumentStore
from .database.vector_store import VectorStore
from .scraper.page_scraper import scrape_article
from .scraper.save_html import save_html_by_article_number
from .scraper.url_collector import generate_medlineplus_urls
from .processor.chunker import chunk_sections
from .processor.extractor import extract_relevant_sections
from app.core.embeddings import EmbeddingGenerator
from app.core.processor import FireworksProcessor
from app.config import *

class Crawler:
    def __init__(self, sleep_interval: float = 1.0):
        self.document_store = DocumentStore()
        self.vector_store = VectorStore( use_faiss = True)
        self.sleep_interval = sleep_interval
        
        self.embedding_generator = EmbeddingGenerator(
            model_id=FIREWORKS_EMBEDDING_MODEL,
            api_key=FIREWORKS_API_KEY,
            url=EMBEDDING_URL
        )
        
        self.process_model = FireworksProcessor(
            model_id=FIREWORKS_MODEL_ID,
            api_key=FIREWORKS_API_KEY,
            api_url=API_URL
        )
        
        # Colas para comunicación entre hilos
        self.url_queue = queue.Queue()
        self.html_queue = queue.Queue()
        self.parsed_queue = queue.Queue()

        self.stop_event = threading.Event()
        self.threads: List[threading.Thread] = []

    def run(self):
        
        workers = [
            threading.Thread(target=self.scraper_worker, daemon=True),
            threading.Thread(target=self.extractor_worker, daemon=True),
            threading.Thread(target=self.embedding_worker, daemon=True),
        ]

        self.threads = workers
        for t in self.threads:
            t.start()

        try:
            while not self.stop_event.is_set():
                time.sleep(self.sleep_interval)
        except KeyboardInterrupt:
            print("Detención solicitada. Parando crawler...")
            self.stop()

    def stop(self):
        self.stop_event.set()
        # Insertar None en colas para desbloquear hilos bloqueados en get()
        for q in [self.url_queue, self.html_queue, self.parsed_queue]:
            q.put(None)

        # Esperar que hilos finalicen
        for t in self.threads:
            t.join(timeout=5)

        # Limpiar tareas pendientes
        self.flush_remaining_tasks()
        print("Crawler detenido correctamente.")

    def scraper_worker(self):
        """ Hilo encargado de obtener el código HTML de los artículos que aún no se han descargado
            o que superaron el tiempo de expiración.
        """
        try:
            for url in generate_medlineplus_urls():
                if self.stop_event.is_set():
                    break
                if self.document_store.check_url_expiration(url):
                    try:
                        html = scrape_article(url)
                    except Exception as e:
                        print(f"Error al descargar HTML de {url}:\n{e}")
                        continue
                    if html:
                        save_html_by_article_number(url, html)
                        self.document_store.record_url_download(url)
                        self.html_queue.put((url, html))                    
        except Exception as e:
            print(f"[scraper_worker] Error inesperado: {e}")
        finally:
            self.html_queue.put(None)

    def extractor_worker(self):
        """
        Hilo encargado de tomar el código html de los artículos descargados y procesarlos.
    
        El procesado incluye:  
            - extraer el contenido de las secciones importantes: nombre, causas, sintomas,...
            - guardar en la base de datos de los documentos los metadatos obtenidos
        """
        while not self.stop_event.is_set():
            item = self.html_queue.get()
            if item is None:
                break
            url, html = item
            try:
                sections = extract_relevant_sections(html)
                if sections:
                    self.document_store.upsert_document(
                        url=url,
                        titulo=sections.get("enfermedad", ""),
                        causas=sections.get("causas", ""),
                        sintomas=sections.get("sintomas", ""),
                        nombres_alternativos=sections.get("nombres_alternativos", "")
                    )
                    self.parsed_queue.put((url, sections))
            except Exception as e:
                print(f"[extractor_worker] Error procesando {url}: {e}")
            finally:
                self.html_queue.task_done()
        self.parsed_queue.put(None)

    def embedding_worker(self):
        """Hilo encargado de tomar los metadatos de los artículos rocesados:
        - dividir en chunks y metadatos
        - guardar los embeddings y los metadatos de los chunks en la base de datos.
        """
        while not self.stop_event.is_set():
            item = self.parsed_queue.get()
            if item is None:
                break
            url, sections = item
            try:
                self._process_and_store_chunks(url, sections)
            except Exception as e:
                print(f"[embedding_worker] Error generando embeddings para {url}: {e}")
            finally:
                self.parsed_queue.task_done()

    def _process_and_store_chunks(self, url: str, sections: dict):
        """
        Procesa las secciones de un artículo, genera los embeddings de los chunks y
        los almacena en la base vectorial junto con sus metadatos.

        Args:
            url (str): URL del artículo original.
            sections (Dict[str, str]): Diccionario con las secciones del artículo.
        """
        embeddings = []
        try:
            chunks, metadatas = chunk_sections(sections, self.process_model)
        except Exception as e:
            raise Exception(f"Error al obtener chunhs: {e}")
            
        if not chunks:
            return

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        chunks = [chunk for chunk in chunks if self.vector_store.get_by_chunk(chunk) is not None]
=======
        # chunks = [chunk for chunk in chunks if self.vector_store.get_by_chunk(chunk) is not None] #Quitar chunks repetidos
>>>>>>> 1416fff (only the GUI needs to be fixed)
        try:
            for batch in batch_chunks(chunks):
                for retry in range(6):
=======
        try:
            for batch in batch_chunks(chunks):
                for retry in range(5):
>>>>>>> 9e4a382 (Bug fixes in the Crawler)
=======
        chunks = [chunk for chunk in chunks if self.vector_store.get_by_chunk(chunk) is not None]
        try:
            for batch in batch_chunks(chunks):
                for retry in range(6):
>>>>>>> bf9eccf (Knowledge Graph)
                    try:
                        batch_embeddings = self.embedding_generator.embed_texts(batch)
                        embeddings.extend(batch_embeddings)
                        break
                    except Exception as e:
                        wait = 2 ** retry
<<<<<<< HEAD
<<<<<<< HEAD
                        print(f"Error (intento {retry+1}/6): {e}. Reintentando en {wait}s...")
=======
                        print(f"Error (intento {retry+1}/5): {e}. Reintentando en {wait}s...")
>>>>>>> 9e4a382 (Bug fixes in the Crawler)
=======
                        print(f"Error (intento {retry+1}/6): {e}. Reintentando en {wait}s...")
>>>>>>> bf9eccf (Knowledge Graph)
                        time.sleep(wait)
                else:
                    print("Fallo permanente al generar embeddings para un batch.")
        except Exception as e:
            print(f"Error inesperado al generar embeddings: {e}")
            
        for idx, (chunk, embedding, meta) in enumerate(zip(chunks, embeddings, metadatas)):
            try:
                self.vector_store.upsert_vector(
                    url=url,
                    chunk_index=idx,
                    text_chunk=chunk,
                    embedding=embedding,
                    nombre=meta.get("nombre"),
                    causa=meta.get("causa"),
                    sintoma=meta.get("sintoma")
                )
            except Exception as e:
                print(f"[embedding_worker] Error almacenando vector chunk {idx} para {url.split('/')[-1]}:\n{e}")

    def process_html_directory(self, html_dir: str = "data/html_docs/",init_id = 0, final_id = 3108):
        """
        Procesa todos los archivos .html en un directorio desde el parseo hasta
        el almacenamiento de embeddings.

        Args:
            html_dir (str): Ruta al directorio que contiene los archivos HTML.
        """
        files = os.listdir(html_dir)
        files.sort()
        for filename in files[init_id:final_id]:
            if not filename.endswith(".html"):
                continue
            
            filepath = os.path.join(html_dir, filename)
            
            url = f"https://medlineplus.gov/spanish/ency/article/{filename}"
            
            if self.document_store.check_url_expiration(url, 30):
                print(f"Procesando articulo: {filename}")
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        html = f.read()

                    if not html:
                        print(f"Articulo {filename} vacio o corrupto")
                        continue
                    
                    secciones = extract_relevant_sections(html)
                    if not secciones:
                        print(f"Advertencia: no se pudieron extraer secciones del articulos {filename}")
                        continue

                    self.document_store.upsert_document(
                        url=url,
                        titulo=secciones.get("enfermedad", ""),
                        causas=secciones.get("causas", ""),
                        sintomas=secciones.get("sintomas", ""),
                        nombres_alternativos=secciones.get("nombres_alternativos", "")
                    )
                    self._process_and_store_chunks(url, secciones)
                    
                except Exception as e:
                    print(f"Error procesando {filename}: {e}")
                    break

    def flush_remaining_tasks(self):
        try:
            self.html_queue.join()
        except Exception:
            pass
        try:
            self.parsed_queue.join()
        except Exception:
            pass

def batch_chunks(chunks, batch_size=128):
    """Agrupar los chunks en grupos de 128 chunks para las peticiones

    Args:
        chunks (list): lista de todos los chunks
        batch_size (int, optional): tamaño de los bloques en que se agruparan los chunks.

    Yields:
        retorna cada uno de los bloques de chunks
    """
    for i in range(0, len(chunks), batch_size):
        yield chunks[i:i + batch_size]