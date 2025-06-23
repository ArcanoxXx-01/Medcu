import threading
import sqlite3
import numpy as np
import faiss
import os
from typing import List, Optional

class VectorStore:
    def __init__(
        self,
        db_path: str = "data/embeddings.db",
        faiss_index_path: str = "data/embeddings.index",
        embedding_dim: int = 768,
        use_faiss: bool = True
    ):
        self.db_path = db_path
        self.embedding_dim = embedding_dim
        self.use_faiss = use_faiss
        self.faiss_index_path = faiss_index_path

        self._local = threading.local()
        self._faiss_lock = threading.Lock()

        self._init_db()
        self._init_faiss()
        self.rebuild_faiss_index_from_db()
        self.save_faiss_index()

    def _get_connection(self) -> sqlite3.Connection:
        if not hasattr(self._local, "conn"):
            self._local.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self._local.conn.row_factory = sqlite3.Row
        return self._local.conn

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vectors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                chunk_index INTEGER NOT NULL,
                text_chunk TEXT NOT NULL,
                embedding BLOB NOT NULL,
                nombre TEXT,
                causa TEXT,
                sintoma TEXT
            )
        """)
        conn.commit()
        conn.close()

    def _init_faiss(self):
        if not self.use_faiss:
            self.faiss_index = None
            return

        if self.faiss_index_path and os.path.exists(self.faiss_index_path):
            try:
                index = faiss.read_index(self.faiss_index_path)
                if index.d != self.embedding_dim:
                    raise ValueError("Dimensión FAISS no coincide con embedding_dim")
                if not isinstance(index, faiss.IndexIDMap):
                    print("[INFO] Reempaquetando índice plano en IndexIDMap")
                    id_map = faiss.IndexIDMap(index)
                    self.faiss_index = id_map
                else:
                    self.faiss_index = index
                return
            except Exception as e:
                print(f"Fallo al cargar índice FAISS: {e}")

        self.rebuild_faiss_index_from_db()
        self.save_faiss_index()

    def rebuild_faiss_index_from_db(self):
        if not self.use_faiss:
            return

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, embedding FROM vectors")
        rows = cursor.fetchall()

        embeddings = []
        ids = []
        for row in rows:
            embedding_bytes = row["embedding"]
            embedding_np = np.frombuffer(embedding_bytes, dtype=np.float32)
            if embedding_np.shape[0] == self.embedding_dim:
                embeddings.append(embedding_np)
                ids.append(row["id"])

        if embeddings:
            embeddings_np = np.array(embeddings).astype(np.float32)
            ids_np = np.array(ids, dtype=np.int64)
        else:
            embeddings_np = np.empty((0, self.embedding_dim), dtype=np.float32)
            ids_np = np.empty((0,), dtype=np.int64)

        with self._faiss_lock:
            base_index = faiss.IndexFlatL2(self.embedding_dim)
            self.faiss_index = faiss.IndexIDMap(base_index)
            if embeddings_np.shape[0] > 0:
                self.faiss_index.add_with_ids(embeddings_np, ids_np)
                

    def upsert_vector(self, url: str, chunk_index: int, text_chunk: str, embedding: List[float], nombre: Optional[str] = None, causa: Optional[str] = None, sintoma: Optional[str] = None):
        conn = self._get_connection()
        cursor = conn.cursor()
        embedding_np = np.array(embedding, dtype=np.float32)
        embedding_bytes = embedding_np.tobytes()

        cursor.execute("""
            INSERT INTO vectors (url, chunk_index, text_chunk, embedding, nombre, causa, sintoma)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (url, chunk_index, text_chunk, embedding_bytes, nombre, causa, sintoma))
        conn.commit()

        if self.use_faiss and self.faiss_index is not None:
            with self._faiss_lock:
                last_id = cursor.lastrowid
                self.faiss_index.add_with_ids(np.expand_dims(embedding_np, axis=0), np.array([last_id], dtype=np.int64))
                

    def search(self, query_embedding: List[float], top_k: int = 5):
        """
        Busca los top_k vectores más similares a la consulta y devuelve
        información básica con la distancia.

        Returns:
            List de tuplas (url, chunk_index, text_chunk, distance)
        """        
        if not self.use_faiss or self.faiss_index is None:
            return []
        
        query_np = np.array(query_embedding, dtype=np.float32).reshape(1, -1)

        try:
            with self._faiss_lock:
                distances, indices = self.faiss_index.search(query_np, top_k)
                # print("IDs devueltos por FAISS:", indices[0])
        except Exception as e:
            print(f"Error en la búsqueda de FAISS: {e}")
            return []

        result_ids= indices[0].tolist()
        conn = self._get_connection()
        cursor = conn.cursor()

        results = []
        
        placeholders= ','.join(['?']*len(result_ids))
        cursor.execute(f"SELECT nombre, sintoma, causa FROM vectors where id IN ({placeholders})", result_ids)
        objects = cursor.fetchall()
        for obj in objects:
            results.append({
                'nombre': obj['nombre'], 
                'causa': obj['causa'], 
                'sintoma': obj['sintoma']
                })
        # print(results)
        return results

    def get_by_chunk(self, chunk: str) -> Optional[dict]:
        """Busca si existe alguna fila en la base de datos que tenga exactamente el mismo texto en la columna text_chunk.

        Args:
            chunk (str): Texto por el cual se compararán los chunks de la base de datos.

        Returns:
            Optional[dict]: Retorna la fila como diccionario si se encuentra una coincidencia exacta, o None en caso contrario.
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT nombre, causa, sintoma FROM vectors WHERE text_chunk = ?", (chunk,))
        row = cursor.fetchone()

        conn.close()

        return dict(row) if row else None


    def save_faiss_index(self, path: str = "data/embeddings.index"):
        """
        Guarda el índice FAISS en disco para persistencia.
        """
        if not self.use_faiss or self.faiss_index is None:
            return

        save_path = path if path else self.faiss_index_path
        with self._faiss_lock:
            faiss.write_index(self.faiss_index, save_path)
