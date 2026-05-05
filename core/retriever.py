"""
Retrieval (veri çekme) stratejileri.
Metadata filtresi, bölüm blok çekme, similarity fallback ve 
genel RAG retriever fonksiyonlarını içerir.
"""

from langchain_chroma import Chroma

from config import (
    RETRIEVER_SEARCH_TYPE,
    RETRIEVER_K,
    RETRIEVER_FETCH_K,
    RETRIEVER_LAMBDA_MULT,
    SIMILARITY_SEARCH_K,
)


def get_retriever(vectorstore: Chroma):
    """MMR tabanlı ana retriever'ı oluştur."""
    return vectorstore.as_retriever(
        search_type=RETRIEVER_SEARCH_TYPE,
        search_kwargs={
            "k": RETRIEVER_K,
            "fetch_k": RETRIEVER_FETCH_K,
            "lambda_mult": RETRIEVER_LAMBDA_MULT,
        },
    )


def detay_getir_metadata(vectorstore: Chroma, isim: str, metadata_key: str) -> str | None:
    """
    metadata_key alanında tam eşleşme yaparak o başlığa ait
    TÜM chunk'ları getirir — chunk boyutundan bağımsız, eksiksiz içerik.
    """
    sonuclar = vectorstore.get(
        where={metadata_key: {"$eq": isim}},
        include=["documents", "metadatas"],
    )
    docs = sonuclar.get("documents", [])
    return "\n\n---\n\n".join(docs) if docs else None


def bolum_getir(vectorstore: Chroma, bolum_adi: str) -> str | None:
    """
    Bolum metadata alanına göre bir bölüme ait TÜM chunk'ları getirir.
    "Hobiler", "Karakteristik Yapı", "Akademik Eğitim" gibi tam bölüm
    sorgularında kullanılır.
    """
    sonuclar = vectorstore.get(
        where={"Bolum": {"$eq": bolum_adi}},
        include=["documents", "metadatas"],
    )
    docs = sonuclar.get("documents", [])
    return "\n\n---\n\n".join(docs) if docs else None


def detay_getir_similarity(vectorstore: Chroma, isim: str) -> str:
    """Metadata filtresi sonuç vermediğinde fallback: similarity search."""
    docs = vectorstore.similarity_search(isim, k=SIMILARITY_SEARCH_K)
    return "\n\n---\n\n".join(
        f"[{d.metadata.get('Bolum', '')} > "
        f"{d.metadata.get('Alt_Bolum', '') or d.metadata.get('Proje_Detay', '')}]\n"
        f"{d.page_content}"
        for d in docs
    )


def format_docs_with_meta(docs) -> str:
    """
    RAG retriever sonuçlarını zengin metadata başlıklarıyla formatlar.
    [Bölüm > Alt Bölüm] şeklinde header ekler.
    """
    result = []
    for doc in docs:
        meta = doc.metadata
        bolum = meta.get("Bolum", "")
        alt = meta.get("Alt_Bolum", "") or meta.get("Proje_Detay", "")
        header = f"[{bolum}{' > ' + alt if alt else ''}]"
        result.append(f"{header}\n{doc.page_content}")
    return "\n\n---\n\n".join(result)
