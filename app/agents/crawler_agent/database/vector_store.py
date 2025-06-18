import threading
import sqlite3
import numpy as np
import faiss
from typing import List, Optional

class VectorStore:
    """
    Gestión de vectores embebidos para documentos médicos usando SQLite para metadatos
    y FAISS para indexación vectorial eficiente.

    Esta clase es segura para multihilo, usa conexiones SQLite por hilo y
    protege acceso a FAISS con un lock.
    """

    def __init__(
        self,
        db_path: str ="data/embeddings.db",
        faiss_index_path: Optional[str] = "data/embeddings.index",
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

        if self.faiss_index_path:
            try:
                self.faiss_index = faiss.read_index(self.faiss_index_path)
                # Validar que dimensión coincida
                if self.faiss_index.d != self.embedding_dim:
                    raise ValueError("Dimensión FAISS no coincide con embedding_dim")
            except Exception:
                # Si falla leer índice, crear uno nuevo
                self.faiss_index = faiss.IndexFlatL2(self.embedding_dim)
        else:
            self.faiss_index = faiss.IndexFlatL2(self.embedding_dim)

    def upsert_vector(
        self,
        url: str,
        chunk_index: int,
        text_chunk: str,
        embedding: List[float],
        nombre: Optional[str] = None,
        causa: Optional[str] = None,
        sintoma: Optional[str] = None
    ):
        """
        Inserta o actualiza un vector y su metadata en la base de datos y FAISS.

        Args:
            url (str): URL del documento.
            chunk_index (int): Índice del chunk dentro del documento.
            text_chunk (str): Texto del chunk.
            embedding (List[float]): Vector embebido.
            nombre (Optional[str]): Metadata adicional.
            causa (Optional[str]): Metadata adicional.
            sintoma (Optional[str]): Metadata adicional.
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        # Convertir embedding a bytes
        embedding_np = np.array(embedding, dtype=np.float32)
        embedding_bytes = embedding_np.tobytes()

        # Insertar o actualizar
        cursor.execute("""
            INSERT INTO vectors (url, chunk_index, text_chunk, embedding, nombre, causa, sintoma)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (url, chunk_index, text_chunk, embedding_bytes, nombre, causa, sintoma))
        conn.commit()

        # Añadir a FAISS con lock para seguridad
        if self.use_faiss and self.faiss_index is not None:
            with self._faiss_lock:
                self.faiss_index.add(np.expand_dims(embedding_np, axis=0))

    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5
    ) -> list[str]:
        """
        Busca los top_k vectores más similares a la consulta y devuelve
        información básica con la distancia.

        Returns:
            List de tuplas (url, chunk_index, text_chunk, distance)
        """
        if not self.use_faiss or self.faiss_index is None:
            return []

        query_np = np.array(query_embedding, dtype=np.float32).reshape(1, -1)

        with self._faiss_lock:
            distances, indices = self.faiss_index.search(query_np, top_k)

        conn = self._get_connection()
        cursor = conn.cursor()

        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx == -1:
                continue
            cursor.execute("SELECT url, chunk_index, text_chunk FROM vectors WHERE id = ?", (idx+1,))
            row = cursor.fetchone()
            if row:
                results.append(row["text_chunk"])
        return results

    def get_by_chunk(self, chunk: str) -> Optional[dict]:
        """Busca si existe alguna fila en la base de datos que tenga exactamente el mismo texto en la columna text_chunk.

        Args:
            chunk (str): Texto por el cual se compararán los chunks de la base de datos.

        Returns:
            Optional[dict]: Retorna la fila como diccionario si se encuentra una coincidencia exacta, o None en caso contrario.
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Esto es para acceder a los resultados como diccionarios
        cursor = conn.cursor()

        cursor.execute("SELECT nombre, causa, sintoma FROM vectors WHERE text_chunk = ?", (chunk,))
        row = cursor.fetchone()

        conn.close()

        return dict(row) if row else None

    def save_faiss_index(self, path: Optional[str] = None):
        """
        Guarda el índice FAISS en disco para persistencia.
        """
        if not self.use_faiss or self.faiss_index is None:
            return

        save_path = path if path else self.faiss_index_path
        if save_path:
            with self._faiss_lock:
                faiss.write_index(self.faiss_index, save_path)
