"""
Yusuf Ataş — AI Kariyer Asistanı
Premium Streamlit Web Arayüzü

Multi-LLM destekli RAG tabanlı kariyer asistanı.
Modüler mimari ile chat.py'nin tüm güçlü yönlerini barındırır.
"""

import logging
import streamlit as st

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
    MENU_CONFIG,
)
from ui.styles import get_custom_css
from ui.components import (
    render_header,
    render_footer,
    render_tip,
)
from ui.sidebar import render_sidebar

# ==========================================
# LOGGING AYARLARI
# ==========================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)

# Kullanıcı girdi sınırı
MAX_INPUT_CHARS = 500

# ==========================================
# SAYFA KONFİGÜRASYONU
# ==========================================
st.set_page_config(
    page_title="Yusuf Ataş | AI Kariyer Asistanı",
    page_icon="👔",
    layout="centered",
    initial_sidebar_state="expanded",
)

# CSS enjeksiyonu
st.markdown(get_custom_css(), unsafe_allow_html=True)


# ==========================================
# SİSTEM BAŞLATMA (Cache ile)
# ==========================================
@st.cache_resource(show_spinner="⏳ Sistem başlatılıyor...")
def init_system():
    """Vectorstore ve LLM Router'ı başlat ve önbelleğe al."""
    vectorstore = get_or_create_vectorstore()
    router = LLMRouter()
    return vectorstore, router


# API anahtarı kontrolü
if not OPENAI_API_KEY:
    st.error(
        "⚠️ OPENAI_API_KEY bulunamadı. "
        "Lütfen `.env` dosyanızı kontrol edin veya ortam değişkeni olarak ekleyin."
    )
    st.stop()

vectorstore, llm_router = init_system()


# ==========================================
# SESSION STATE YÖNETİMİ
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Merhaba! 👋 Ben **Yusuf Ataş**'ın AI Kariyer Asistanıyım.\n\n"
                "Projeleri, iş deneyimleri, sertifikaları, hatta karakteristik "
                "özellikleri hakkında sorular sorabilirsiniz.\n\n"
                "Ayrıca sol menüdeki navigasyonu da kullanabilirsiniz."
            ),
        }
    ]

if "aktif_menu" not in st.session_state:
    st.session_state.aktif_menu = None


# ==========================================
# YARDIMCI FONKSİYONLAR
# ==========================================
def process_question(soru: str) -> str:
    """
    Kullanıcı sorusunu işleyerek yanıt üretir.
    chat.py'nin akış mantığını birebir korur.
    """
    llm = llm_router.get_llm()

    # ── DURUM 1: Menü açık — seçim bekleniyor ──
    if st.session_state.aktif_menu:
        sozluk = SOZLUK_MAP[st.session_state.aktif_menu]
        metadata_key = METADATA_KEY_MAP[st.session_state.aktif_menu]
        secilen = secim_coz(soru, sozluk)

        if secilen:
            # Geçerli seçim → detay getir
            context_str = detay_getir_metadata(vectorstore, secilen, metadata_key)
            if context_str is None:
                context_str = detay_getir_similarity(vectorstore, secilen)

            detay_sorusu = f"{secilen} hakkında detaylı bilgi ver"
            cevap = run_metadata_chain(llm, context_str, detay_sorusu)
            return cevap + "\n\n💡 *Listeden başka bir numara yazabilir veya yeni bir konu sorabilirsiniz.*"

        else:
            # Geçersiz giriş → intent kontrol et
            yeni_intent = intent_tespit(soru)

            if yeni_intent not in ("rag",) and not yeni_intent.startswith("bolum_blok"):
                # Başka menüye geçiş
                st.session_state.aktif_menu = yeni_intent.replace("_menu", "")
                return MENU_MESAJ_MAP[st.session_state.aktif_menu]

            elif yeni_intent == "rag":
                # Serbest soru → menüden çık
                st.session_state.aktif_menu = None
                rag_chain = create_rag_chain(vectorstore, llm)
                return rag_chain.invoke({"soru": soru})

            elif yeni_intent.startswith("bolum_blok"):
                st.session_state.aktif_menu = None
                bolum_adi = yeni_intent.split(":", 1)[1]
                context_str = bolum_getir(vectorstore, bolum_adi)
                if context_str is None:
                    context_str = detay_getir_similarity(vectorstore, soru)
                return run_metadata_chain(llm, context_str, soru)

            else:
                return (
                    f"Anlayamadım, lütfen listeden bir numara veya isim yazın:\n\n"
                    f"{MENU_METNI_MAP[st.session_state.aktif_menu]}"
                )

    # ── DURUM 2: Menü kapalı — intent tespiti ──
    intent = intent_tespit(soru)

    if intent.endswith("_menu"):
        st.session_state.aktif_menu = intent.replace("_menu", "")
        return MENU_MESAJ_MAP[st.session_state.aktif_menu]

    elif intent.startswith("bolum_blok:"):
        bolum_adi = intent.split(":", 1)[1]
        context_str = bolum_getir(vectorstore, bolum_adi)
        if context_str is None:
            context_str = detay_getir_similarity(vectorstore, soru)
        return run_metadata_chain(llm, context_str, soru)

    else:
        # Genel RAG
        st.session_state.aktif_menu = None
        rag_chain = create_rag_chain(vectorstore, llm)
        return rag_chain.invoke({"soru": soru})


# ==========================================
# ARAYÜZ OLUŞTURMA
# ==========================================

# Header
render_header()

# Sidebar (aksiyonları yakala)
sidebar_action = render_sidebar(llm_router)

# Sidebar'dan gelen aksiyon
if sidebar_action:
    if sidebar_action.startswith("bolum:"):
        # Bölüm sorgusu (Teknik, Eğitim vb.)
        bolum_adi = sidebar_action.split(":", 1)[1]
        prompt_text = f"{bolum_adi} hakkında bilgi ver"
        st.session_state.messages.append({"role": "user", "content": prompt_text})
        st.session_state.aktif_menu = None
        # Yanıtı hesapla ve ekle
        llm = llm_router.get_llm()
        context_str = bolum_getir(vectorstore, bolum_adi)
        if context_str is None:
            context_str = detay_getir_similarity(vectorstore, prompt_text)
        cevap = run_metadata_chain(llm, context_str, prompt_text)
        st.session_state.messages.append({"role": "assistant", "content": cevap})
        st.rerun()
    else:
        # Menü aksiyonu (proje, deneyim, sertifika, mulakat)
        st.session_state.aktif_menu = sidebar_action
        menu_msg = MENU_MESAJ_MAP[sidebar_action]
        st.session_state.messages.append({"role": "assistant", "content": menu_msg})
        st.rerun()

# Mesaj geçmişini göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ==========================================
# KULLANICI GİRDİSİ VE CEVAP DÖNGÜSÜ
# ==========================================
if user_input := st.chat_input("Mesajınızı buraya yazabilirsiniz..."):
    soru = user_input.strip()

    if not soru:
        st.stop()

    # Karakter sınırı kontrolü
    if len(soru) > MAX_INPUT_CHARS:
        st.warning(f"⚠️ Mesajınız çok uzun ({len(soru)}/{MAX_INPUT_CHARS} karakter). Lütfen daha kısa bir soru sorun.")
        st.stop()

    # İptal komutları
    if soru.lower() in {"iptal", "vazgeç", "geri", "ana menü"}:
        st.session_state.aktif_menu = None
        cancel_msg = "Başka bir konuda yardımcı olabilir miyim?"
        st.session_state.messages.append({"role": "user", "content": soru})
        st.session_state.messages.append({"role": "assistant", "content": cancel_msg})
        st.rerun()

    # Kullanıcı mesajını ekle
    st.session_state.messages.append({"role": "user", "content": soru})
    with st.chat_message("user"):
        st.markdown(soru)

    # Yanıt oluştur
    with st.chat_message("assistant"):
        with st.spinner("Düşünüyor..."):
            try:
                cevap = process_question(soru)
                
                # Daktilo efekti için basit bir jeneratör
                def stream_data(text):
                    import time
                    for word in text.split(" "):
                        yield word + " "
                        time.sleep(0.05)
                
                # Yanıtı akış olarak yazdır
                full_response = st.write_stream(stream_data(cevap))
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                logger.error(f"Soru işleme hatası: {e}", exc_info=True)
                error_msg = f"⚠️ Bir hata oluştu: {e}\n\nLütfen tekrar deneyin."
                st.markdown(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Footer
render_footer()