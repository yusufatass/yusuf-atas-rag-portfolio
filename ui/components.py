"""
Yeniden kullanılabilir Streamlit arayüz bileşenleri.
Header, durum kartları, menü göstergesi ve örnek promptlar.
"""

import streamlit as st


def render_header():
    """Gradient banner ile sayfa başlığını oluşturur."""
    st.markdown("""
        <div class="header-container">
            <div class="header-title">👔 Yusuf Ataş</div>
            <div class="header-subtitle">AI Kariyer Asistanı — Yapay Zeka Destekli Profesyonel Profil Sistemi</div>
            <div class="header-badge">&#129302; RAG-Powered Assistant</div>
        </div>
    """, unsafe_allow_html=True)


def render_provider_status(status: dict[str, str]):
    """LLM sağlayıcılarının durumunu sidebar'da gösterir."""
    for provider, state in status.items():
        is_active = "Aktif" in state
        css_class = "provider-card-active" if is_active else ""
        icon = provider.capitalize()
        st.markdown(
            f'<div class="provider-card {css_class}">'
            f'<strong>{icon}:</strong> {state}</div>',
            unsafe_allow_html=True,
        )


def render_menu_badge(menu_name: str | None):
    """Aktif menü durumunu gösterir."""
    menu_labels = {
        "proje": "🚀 Proje Menüsü",
        "deneyim": "💼 Deneyim Menüsü",
        "sertifika": "📜 Sertifika Menüsü",
        "mulakat": "🎯 Mülakat Menüsü",
    }

    if menu_name and menu_name in menu_labels:
        st.markdown(
            f'<div class="menu-badge">{menu_labels[menu_name]} aktif</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="menu-badge-inactive">💬 Serbest sohbet modu</div>',
            unsafe_allow_html=True,
        )


def render_example_chips():
    """Yeni kullanıcılar için örnek prompt butonlarını gösterir."""
    examples = [
        ("🚀 Projeler", "Projelerini listele"),
        ("💼 Deneyim", "İş deneyimlerini anlat"),
        ("📜 Sertifikalar", "Hangi sertifikaları var?"),
        ("🎯 Mülakat", "Mülakat soruları"),
        ("🧠 Teknik", "Teknik yetkinlikleri neler?"),
        ("🎓 Eğitim", "Akademik eğitimi hakkında bilgi ver"),
    ]

    cols = st.columns(3)
    selected = None

    for i, (label, prompt) in enumerate(examples):
        col_idx = i % 3
        with cols[col_idx]:
            if st.button(label, key=f"chip_{i}", use_container_width=True):
                selected = prompt

    return selected


def render_footer():
    """Sayfa alt bilgisini oluşturur."""
    st.markdown("""
        <div class="footer">
            <a href="mailto:yusufatas2002@gmail.com">📧 E-posta</a> · 
            <a href="https://linkedin.com/in/yusuf-atas34" target="_blank">💼 LinkedIn</a> · 
            <a href="https://github.com/yusufatass" target="_blank">💻 GitHub</a>
            <br>
            <span style="font-size: 0.7rem; margin-top: 0.3rem; display: inline-block;">
                Multi-LLM RAG Architecture · Powered by LangChain & ChromaDB
            </span>
        </div>
    """, unsafe_allow_html=True)


def render_tip(text: str):
    """İpucu kutucuğu gösterir."""
    st.markdown(
        f'<div class="tip-box">💡 {text}</div>',
        unsafe_allow_html=True,
    )
