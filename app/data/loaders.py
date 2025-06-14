import os
import faiss
import pickle

GLOBAL_INDEX_DIR = "app/data/vector_index"

def load_global_index():
    try:
        index_path = os.path.join(GLOBAL_INDEX_DIR, "index.faiss")
        meta_path = os.path.join(GLOBAL_INDEX_DIR, "metadata.pkl")

        index = faiss.read_index(index_path)
        with open(meta_path, "rb") as f:
            metadata = pickle.load(f)

        return index, metadata
    except Exception as e:
        print(f"Error cargando índice global: {e}")
        return None, []
