"""
ChromaDB vektör veritabanı yönetimi.
Hash tabanlı önbellekleme ile gereksiz yeniden indekslemeyi önler.
"""

import hashlib
import shutil
from pathlib import Path

from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpointEmbeddings
from langchain_chroma import Chroma

from config import (
    CHROMA_DIR,
    CHROMA_COLLECTION_NAME,
    SOURCE_HASH_FILE,
    KNOWLEDGE_BASE_FILE,
    EMBEDDING_MODEL_NAME,
    EMBEDDING_DEVICE,
    EMBEDDING_NORMALIZE,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    CHUNK_SEPARATORS,
    MARKDOWN_HEADERS,
    HF_TOKEN,
)


def _get_embeddings_model():
    """
    Embedding modelini oluştur ve döndür.
    HF_TOKEN varsa API üzerinden, yoksa yerelden çalışır.
    """
    if HF_TOKEN:
        print("🚀 Hugging Face Inference API kullanılıyor...")
        return HuggingFaceEndpointEmbeddings(
            model=EMBEDDING_MODEL_NAME,
            huggingfacehub_api_token=HF_TOKEN,
        )
    
    print("💻 Yerel embedding modeli kullanılıyor...")
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs={"device": EMBEDDING_DEVICE},
        encode_kwargs={"normalize_embeddings": EMBEDDING_NORMALIZE},
    )


def _compute_file_hash(file_path: Path) -> str:
    """Dosyanın MD5 hash'ini hesapla."""
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _read_stored_hash() -> str | None:
    """Kayıtlı hash'i oku. Yoksa None döndür."""
    if SOURCE_HASH_FILE.exists():
        return SOURCE_HASH_FILE.read_text(encoding="utf-8").strip()
    return None


def _write_hash(hash_value: str) -> None:
    """Hash değerini diske yaz."""
    SOURCE_HASH_FILE.parent.mkdir(parents=True, exist_ok=True)
    SOURCE_HASH_FILE.write_text(hash_value, encoding="utf-8")


def needs_reindex(data_path: Path | None = None) -> bool:
    """
    Yeniden indeksleme gerekli mi?
    - chroma_db yoksa → True
    - Hash dosyası yoksa → True
    - Hash uyuşmuyorsa → True
    - Hepsi uygunsa → False
    """
    data_path = data_path or KNOWLEDGE_BASE_FILE

    if not CHROMA_DIR.exists():
        return True

    stored_hash = _read_stored_hash()
    if stored_hash is None:
        return True

    current_hash = _compute_file_hash(data_path)
    return stored_hash != current_hash


def build_index(data_path: Path | None = None, force: bool = False) -> Chroma:
    """
    Vektör veritabanını oluştur veya yükle.
    
    Args:
        data_path: Kaynak markdown dosyası yolu
        force: True ise mevcut DB'yi sil ve yeniden oluştur
    
    Returns:
        Chroma vectorstore instance
    """
    data_path = data_path or KNOWLEDGE_BASE_FILE
    embeddings = _get_embeddings_model()

    if not force and not needs_reindex(data_path):
        print("✅ Mevcut veritabanı güncel — yükleniyor...")
        return Chroma(
            persist_directory=str(CHROMA_DIR),
            embedding_function=embeddings,
            collection_name=CHROMA_COLLECTION_NAME,
        )

    # Yeniden indeksleme gerekli — önce ChromaDB bağlantısını kapat
    if CHROMA_DIR.exists():
        try:
            # ChromaDB dosya tutamaçlarını serbest bırak
            _tmp = Chroma(
                persist_directory=str(CHROMA_DIR),
                embedding_function=embeddings,
                collection_name=CHROMA_COLLECTION_NAME,
            )
            _tmp.delete_collection()
            del _tmp
        except Exception:
            pass  # Zaten bozuksa geç

        # Şimdi dizini güvenle sil (retry ile)
        import time
        for attempt in range(5):
            try:
                shutil.rmtree(CHROMA_DIR)
                break
            except PermissionError:
                time.sleep(0.5)
        print("🗑️  Eski veritabanı silindi.")

    print(f"📄 Kaynak dosya okunuyor: {data_path.name}")
    markdown_text = data_path.read_text(encoding="utf-8")

    # Markdown başlık bölme
    md_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=MARKDOWN_HEADERS,
        strip_headers=False,
    )
    md_splits = md_splitter.split_text(markdown_text)

    # Recursive karakter bölme
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=CHUNK_SEPARATORS,
    )
    final_chunks = text_splitter.split_documents(md_splits)
    print(f"✅ {len(final_chunks)} chunk oluşturuldu.")

    # ChromaDB'ye yaz
    print("⏳ Vektör veritabanı oluşturuluyor...")
    vectorstore = Chroma.from_documents(
        documents=final_chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR),
        collection_name=CHROMA_COLLECTION_NAME,
    )
    print(f"✅ {len(final_chunks)} chunk veritabanına yazıldı.")

    # Hash'i kaydet
    current_hash = _compute_file_hash(data_path)
    _write_hash(current_hash)
    print("✅ Kaynak dosya hash'i kaydedildi.")

    return vectorstore


def get_or_create_vectorstore() -> Chroma:
    """
    Uygulama başlangıcında kullanılacak tek giriş noktası.
    Mevcut DB varsa yükler, yoksa oluşturur.
    """
    embeddings = _get_embeddings_model()

    if not needs_reindex():
        return Chroma(
            persist_directory=str(CHROMA_DIR),
            embedding_function=embeddings,
            collection_name=CHROMA_COLLECTION_NAME,
        )

    # Otomatik indeksleme
    return build_index()


def get_embeddings() -> HuggingFaceEmbeddings:
    """Embedding modeline dışarıdan erişim."""
    return _get_embeddings_model()
