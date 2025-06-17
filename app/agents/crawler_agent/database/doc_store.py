import sqlite3
import threading
from datetime import datetime
from typing import Optional

class DocumentStore:
    """
    Gestor de documentos médicos en SQLite, seguro para entornos multihilo.
    Cada hilo mantiene su propia conexión a la base de datos.
    """

    def __init__(self, db_path: str ="data/documents.db"):
        self.db_path = db_path
        self._local = threading.local()
        self._init_schema()

    def _get_connection(self) -> sqlite3.Connection:
        """
        Obtiene una conexión SQLite específica del hilo actual.
        """
        if not hasattr(self._local, "conn"):
            self._local.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self._local.conn.row_factory = sqlite3.Row
        return self._local.conn

    def _init_schema(self):
        """
        Crea las tablas necesarias si no existen. Ejecutado una sola vez desde el hilo principal.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS downloaded_urls (
                url TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                url TEXT PRIMARY KEY,
                titulo TEXT,
                causas TEXT,
                sintomas TEXT,
                primeros_auxilios TEXT,
                no_se_debe TEXT,
                nombres_alternativos TEXT,
                ejemplo_comsulta TEXT,
                timestamp TEXT NOT NULL
            )
        """)

        conn.commit()
        conn.close()

    def was_url_downloaded(self, url: str) -> bool:
        """Verifica si una URL ya ha sido descargada previamente.

        Args:
            url (str): url del artículo

        Returns:
            bool: representa si ya se descargó el artículo
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM downloaded_urls WHERE url = ?", (url,))
        return cursor.fetchone() is not None

    def record_url_download(self, url: str):
        """
        Registra que una **URL** fue descargada, con **`timestamp`** actual.
        
        Args:
            url (str): url del artículo
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO downloaded_urls (url, timestamp) VALUES (?, ?)",
            (url, datetime.utcnow().isoformat())
        )
        conn.commit()

    def upsert_document(
        self,
        url: str,
        titulo: Optional[str],
        causas: Optional[str],
        sintomas: Optional[str],
        primeros_auxilios: Optional[str],
        no_se_debe: Optional[str],
        nombres_alternativos: Optional[str],
        ejemplo_comsulta: Optional[str]
    ):
        """
        Inserta o actualiza un documento médico completo.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO documents (
                url, titulo, causas, sintomas, primeros_auxilios,
                no_se_debe, nombres_alternativos, ejemplo_comsulta, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            url,
            titulo or "",
            causas or "",
            sintomas or "",
            primeros_auxilios or "",
            no_se_debe or "",
            nombres_alternativos or "",
            ejemplo_comsulta or "",
            datetime.utcnow().isoformat()
        ))
        conn.commit()

    def get_html_path(url: str) -> str:
        """
        Devuelve la ruta local al archivo HTML asociado a la URL dada.
        Asume un patrón de almacenamiento basado en el hash de la URL.
        """
        import os
        return os.path.join("data", "html_docs", url.split('/')[-1])

db = DocumentStore("prueba.db")

db.upsert_document()