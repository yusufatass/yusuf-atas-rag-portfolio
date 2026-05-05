"""
Vektör veritabanı indeksleme betiği.
Kaynak .md dosyası değişmediyse mevcut DB'yi kullanır.
--force bayrağı ile zorla yeniden indeksleme yapılabilir.

Kullanım:
    python main.py          # Akıllı indeksleme (hash kontrolü)
    python main.py --force  # Zorla yeniden indeksleme
"""

import sys
from config import KNOWLEDGE_BASE_FILE, RETRIEVER_SEARCH_TYPE, RETRIEVER_K, RETRIEVER_FETCH_K, RETRIEVER_LAMBDA_MULT
from core.vectorstore import build_index, needs_reindex


def main():
    force = "--force" in sys.argv

    if not KNOWLEDGE_BASE_FILE.exists():
        print(f"❌ Kaynak dosya bulunamadı: {KNOWLEDGE_BASE_FILE}")
        sys.exit(1)

    if not force and not needs_reindex():
        print("✅ Veritabanı güncel — yeniden indeksleme gerekmez.")
        print("   Zorla yeniden oluşturmak için: python main.py --force")
        return

    print("=" * 55)
    print("📦 Vektör Veritabanı İndeksleme Başlatılıyor")
    print("=" * 55)

    vectorstore = build_index(force=force)

    # Sistem testi
    print("\n--- RETRIEVAL TESTİ ---")
    retriever = vectorstore.as_retriever(
        search_type=RETRIEVER_SEARCH_TYPE,
        search_kwargs={
            "k": RETRIEVER_K,
            "fetch_k": RETRIEVER_FETCH_K,
            "lambda_mult": RETRIEVER_LAMBDA_MULT,
        },
    )

    test_sorgu = "Yusuf'un yapay zeka alanındaki projeleri nelerdir?"
    sonuclar = retriever.invoke(test_sorgu)

    print(f"Sorgu: '{test_sorgu}'")
    for i, doc in enumerate(sonuclar, 1):
        print(f"\n[{i}] Metadata : {doc.metadata}")
        print(f"    İçerik   : {doc.page_content[:150]}...")

    print("\n" + "=" * 55)
    print("✅ İndeksleme ve test başarıyla tamamlandı!")
    print("=" * 55)


if __name__ == "__main__":
    main()