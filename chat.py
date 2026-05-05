"""
CLI tabanlı interaktif sohbet arayüzü.
Orijinal chat.py'nin tüm işlevselliğini korur,
ancak tüm mantığı core/ modüllerinden alır.

Kullanım:
    python chat.py
"""

import logging

from config import OPENAI_API_KEY
from core.vectorstore import get_or_create_vectorstore
from core.llm_router import LLMRouter
from core.chains import create_rag_chain, run_metadata_chain
from core.retriever import (
    detay_getir_metadata,
    bolum_getir,
    detay_getir_similarity,
)
from core.intent import (
    intent_tespit,
    secim_coz,
    SOZLUK_MAP,
    METADATA_KEY_MAP,
    MENU_MESAJ_MAP,
    MENU_METNI_MAP,
)

# ==========================================
# LOGGING
# ==========================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    # ==========================================
    # SİSTEM BAŞLATMA
    # ==========================================
    if not OPENAI_API_KEY:
        raise EnvironmentError(
            "OPENAI_API_KEY bulunamadı.\n"
            "PowerShell → $env:OPENAI_API_KEY='senin_anahtarin'\n"
            "CMD        → set OPENAI_API_KEY=senin_anahtarin"
        )

    print("⏳ Asistan uyanıyor...")

    vectorstore = get_or_create_vectorstore()
    router = LLMRouter()
    llm = router.get_llm()
    rag_chain = create_rag_chain(vectorstore, llm)

    # Sağlayıcı durumunu göster
    print("\n📊 LLM Sağlayıcı Durumları:")
    for provider, status in router.get_status().items():
        print(f"   {provider}: {status}")

    print("\n✅ Asistan Hazır! Çıkmak için 'q' yaz.\n")
    print("=" * 55)

    # ==========================================
    # İNTERAKTİF SOHBET DÖNGÜSÜ
    # ==========================================
    aktif_menu: str | None = None

    while True:
        soru = input("\n👤 Sen: ").strip()

        if not soru:
            continue
        if soru.lower() in {"q", "quit", "exit", "çıkış"}:
            print("👋 Görüşmek üzere!")
            break

        # Menüden çıkış
        if soru.lower() in {"iptal", "vazgeç", "geri", "ana menü"}:
            aktif_menu = None
            print("\n🤖 Asistan:\nBaşka bir konuda yardımcı olabilir miyim?")
            print("-" * 55)
            continue

        try:
            # Başarısız sağlayıcı varsa LLM'i yeniden al
            current_llm = router.get_llm()

            # ── DURUM 1: Menü açık — seçim bekleniyor ──
            if aktif_menu:
                sozluk = SOZLUK_MAP[aktif_menu]
                metadata_key = METADATA_KEY_MAP[aktif_menu]
                secilen = secim_coz(soru, sozluk)

                if secilen:
                    context_str = detay_getir_metadata(vectorstore, secilen, metadata_key)
                    if context_str is None:
                        context_str = detay_getir_similarity(vectorstore, secilen)

                    detay_sorusu = f"{secilen} hakkında detaylı bilgi ver"
                    cevap = run_metadata_chain(current_llm, context_str, detay_sorusu)
                    print(f"\n🤖 Asistan:\n{cevap}")
                    print(
                        f"\n💡 İpucu: Listeden başka bir numara yazabilir "
                        f"veya yeni bir konu sorabilirsiniz."
                    )
                else:
                    yeni_intent = intent_tespit(soru)
                    if yeni_intent not in ("rag",) and not yeni_intent.startswith("bolum_blok"):
                        aktif_menu = yeni_intent.replace("_menu", "")
                        print(f"\n🤖 Asistan:\n{MENU_MESAJ_MAP[aktif_menu]}")
                    elif yeni_intent == "rag":
                        aktif_menu = None
                        current_rag_chain = create_rag_chain(vectorstore, current_llm)
                        cevap = current_rag_chain.invoke({"soru": soru})
                        print(f"\n🤖 Asistan:\n{cevap}")
                    elif yeni_intent.startswith("bolum_blok"):
                        aktif_menu = None
                        bolum_adi = yeni_intent.split(":", 1)[1]
                        context_str = bolum_getir(vectorstore, bolum_adi)
                        if context_str is None:
                            context_str = detay_getir_similarity(vectorstore, soru)
                        cevap = run_metadata_chain(current_llm, context_str, soru)
                        print(f"\n🤖 Asistan:\n{cevap}")
                    else:
                        print(
                            f"\n🤖 Asistan:\nAnlayamadım, lütfen listeden bir numara "
                            f"veya isim yazın:\n\n{MENU_METNI_MAP[aktif_menu]}"
                        )

                print("-" * 55)
                continue

            # ── DURUM 2: Menü kapalı — intent tespiti ──
            intent = intent_tespit(soru)

            if intent.endswith("_menu"):
                aktif_menu = intent.replace("_menu", "")
                print(f"\n🤖 Asistan:\n{MENU_MESAJ_MAP[aktif_menu]}")
            elif intent.startswith("bolum_blok:"):
                bolum_adi = intent.split(":", 1)[1]
                context_str = bolum_getir(vectorstore, bolum_adi)
                if context_str is None:
                    context_str = detay_getir_similarity(vectorstore, soru)
                cevap = run_metadata_chain(current_llm, context_str, soru)
                print(f"\n🤖 Asistan:\n{cevap}")
            else:
                aktif_menu = None
                current_rag_chain = create_rag_chain(vectorstore, current_llm)
                cevap = current_rag_chain.invoke({"soru": soru})
                print(f"\n🤖 Asistan:\n{cevap}")

            print("-" * 55)

        except Exception as e:
            logger.error(f"Hata: {e}", exc_info=True)
            print(f"⚠️  Hata: {e}")


if __name__ == "__main__":
    main()