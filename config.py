"""
Merkezi yapılandırma modülü.
Tüm LLM sağlayıcıları, embedding modeli, vektör veritabanı yolları
ve retriever parametreleri burada tanımlanır.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ==========================================
# PROJE YOLLARI & LİMİTLER
# ==========================================
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
CHROMA_DIR = PROJECT_ROOT / "chroma_db"
SOURCE_HASH_FILE = CHROMA_DIR / ".source_hash"
KNOWLEDGE_BASE_FILE = DATA_DIR / "Yusuf_Atas_Kisisel_Bilgi_Tabani.md"
MAX_INPUT_CHARS = 500

# ==========================================
# API ANAHTARLARI
# ==========================================
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
HF_TOKEN = os.environ.get("HUGGINGFACEHUB_API_TOKEN")

# ==========================================
# EMBEDDING MODELİ
# ==========================================
EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
EMBEDDING_DEVICE = "cpu"
EMBEDDING_NORMALIZE = True

# ==========================================
# CHROMA VERİTABANI
# ==========================================
CHROMA_COLLECTION_NAME = "yusuf_atas_cv"

# ==========================================
# CHUNKING PARAMETRELERİ
# ==========================================
CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200
CHUNK_SEPARATORS = ["\n\n", "\n", " ", ""]

MARKDOWN_HEADERS = [
    ("#",    "Ana_Baslik"),
    ("##",   "Bolum"),
    ("###",  "Alt_Bolum"),
    ("####", "Proje_Detay"),
]

# ==========================================
# RETRIEVER PARAMETRELERİ
# ==========================================
RETRIEVER_SEARCH_TYPE = "mmr"
RETRIEVER_K = 6
RETRIEVER_FETCH_K = 15
RETRIEVER_LAMBDA_MULT = 0.7
SIMILARITY_SEARCH_K = 8

# ==========================================
# LLM SAĞLAYICILARI
# ==========================================
LLM_PROVIDERS = {
    "openai": {
        "model": "gpt-4o-mini",
        "temperature": 0.3,
        "api_key_env": "OPENAI_API_KEY",
    },
    "groq": {
        "model": "llama-3.3-70b-versatile",
        "temperature": 0.3,
        "api_key_env": "GROQ_API_KEY",
    },
    "gemini": {
        "model": "gemini-2.0-flash",
        "temperature": 0.3,
        "api_key_env": "GOOGLE_API_KEY",
    },
}

# Öncelik sırası: OpenAI → Groq → Gemini
LLM_PRIORITY = ["openai", "groq", "gemini"]

# Gemini'ye yönlendirme için token eşiği (context çok büyükse)
LARGE_CONTEXT_TOKEN_THRESHOLD = 12000

# Başarısız provider için bekleme süresi (saniye)
PROVIDER_COOLDOWN_SECONDS = 60

# ==========================================
# KULLANILABILIR SAĞLAYICILARI TESPİT ET
# ==========================================

def get_available_providers() -> list[str]:
    """API anahtarı mevcut olan sağlayıcıları döndürür."""
    available = []
    for name in LLM_PRIORITY:
        key_env = LLM_PROVIDERS[name]["api_key_env"]
        if os.environ.get(key_env):
            available.append(name)
    return available
