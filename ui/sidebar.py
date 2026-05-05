"""
Sidebar navigasyon yönetimi.
Kategori butonları, menü durumu göstergesi ve sohbet temizleme.
"""

import streamlit as st

from core.intent import MENU_MESAJ_MAP
from ui.components import render_menu_badge, render_provider_status


def render_sidebar(llm_router=None):
    """
    Sidebar'ı oluşturur ve kullanıcı etkileşimlerini yönetir.
    
    Returns:
        Sidebar'dan seçilen aksiyon:
        - "proje" / "deneyim" / "sertifika" / "mulakat" → menü aç
        - "bolum:..." → bölüm sorgusu tetikle
        - None → aksiyon yok
    """
    with st.sidebar:
        # Logo ve başlık
        st.markdown(
            "<h2 style='text-align:center; font-size:2rem; letter-spacing:0.08em; margin-bottom:0.2rem;'>🧭 NAVİGASYON</h2>",
            unsafe_allow_html=True,
        )
        st.markdown("---")

        # Kategori butonları
        sidebar_action = None

        if st.button("🚀 Projeleri Listele", key="sb_proje", use_container_width=True):
            sidebar_action = "proje"

        if st.button("💼 Deneyimleri Listele", key="sb_deneyim", use_container_width=True):
            sidebar_action = "deneyim"

        if st.button("📜 Sertifikaları Listele", key="sb_sertifika", use_container_width=True):
            sidebar_action = "sertifika"

        if st.button("🎯 İK / Mülakat Soruları", key="sb_mulakat", use_container_width=True):
            sidebar_action = "mulakat"

        if st.button("🧠 Teknik Yetkinlikler", key="sb_teknik", use_container_width=True):
            sidebar_action = "bolum:2. TEKNİK YETKİNLİKLER"

        if st.button("🎓 Akademik Eğitim", key="sb_egitim", use_container_width=True):
            sidebar_action = "bolum:5. AKADEMİK EĞİTİM"

        if st.button("📞 İletişim Bilgileri", key="sb_iletisim", use_container_width=True):
            sidebar_action = "bolum:10. İLETİŞİM BİLGİLERİ"

        st.markdown("---")

        # Aktif menü göstergesi
        st.markdown("## 📌 Durum")
        render_menu_badge(st.session_state.get("aktif_menu"))

        # Menü aktifken iptal butonu
        if st.session_state.get("aktif_menu"):
            if st.button("↩️ Menüden Çık", key="sb_iptal", use_container_width=True):
                st.session_state.aktif_menu = None
                st.rerun()

        st.markdown("---")

        # LLM sağlayıcı durumları
        if llm_router:
            st.markdown("## ⚡ LLM Sağlayıcıları")
            render_provider_status(llm_router.get_status())
            st.markdown("---")

        # Sohbet temizleme
        if st.button("🧹 Sohbeti Temizle", key="sb_temizle", use_container_width=True):
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": (
                        "Sohbet Temizlendi! 👋\n\n"
                        "Projeleri, iş deneyimleri, sertifikaları, hatta karakteristik "
                        "özellikleri hakkında sorular sorabilirsiniz.\n\n"
                        "Ayrıca sol menüdeki navigasyonu da kullanabilirsiniz."
                    ),
                }
            ]
            st.session_state.aktif_menu = None
            st.rerun()

    return sidebar_action
