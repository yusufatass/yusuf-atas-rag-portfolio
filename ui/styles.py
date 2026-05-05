"""
Premium CSS stilleri — Streamlit arayüzü için özel tasarım.
Koyu tema, glassmorphism efektleri, gradient arka planlar
ve mikro-animasyonlar içerir.
"""


def get_custom_css() -> str:
    """Streamlit'e enjekte edilecek premium CSS kodunu döndürür."""
    return """
<style>
    /* =============================================
       GOOGLE FONTS — Inter
       ============================================= */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* =============================================
       GLOBAL TEMA — Koyu Modern
       ============================================= */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* =============================================
       HEADER — Gradient Banner
       ============================================= */
    .header-container {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 30%, #16213e 60%, #0f3460 100%);
        border-radius: 16px;
        padding: 2rem 2.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.06);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        position: relative;
        overflow: hidden;
    }

    .header-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(
            circle at 30% 50%,
            rgba(99, 102, 241, 0.08) 0%,
            transparent 50%
        );
        animation: headerGlow 8s ease-in-out infinite alternate;
    }

    @keyframes headerGlow {
        0% { transform: translate(0, 0); }
        100% { transform: translate(5%, -5%); }
    }

    .header-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.3rem;
        position: relative;
        z-index: 1;
        letter-spacing: -0.02em;
        font-family: 'Inter', "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", sans-serif !important;
    }

    .header-subtitle {
        font-size: 0.95rem;
        color: rgba(255, 255, 255, 0.55);
        position: relative;
        z-index: 1;
        font-weight: 400;
        font-family: 'Inter', sans-serif;
    }

    .header-badge {
        display: inline-block;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-top: 0.5rem;
        position: relative;
        z-index: 1;
        letter-spacing: 0.03em;
        font-family: 'Inter', "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", sans-serif !important;
    }

    /* =============================================
       SIDEBAR — Glass Efekti
       ============================================= */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f1a 0%, #1a1a2e 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
    }

    section[data-testid="stSidebar"] .stMarkdown h2 {
        color: rgba(255, 255, 255, 0.9) !important;
        font-size: 0.85rem !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 600;
    }

    /* Sidebar butonları */
    section[data-testid="stSidebar"] .stButton > button {
        width: 100%;
        background: rgba(99, 102, 241, 0.08) !important;
        border: 1px solid rgba(99, 102, 241, 0.15) !important;
        color: rgba(255, 255, 255, 0.85) !important;
        border-radius: 10px !important;
        padding: 0.6rem 1rem !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        text-align: left !important;
        margin-bottom: 0.3rem !important;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(99, 102, 241, 0.2) !important;
        border-color: rgba(99, 102, 241, 0.4) !important;
        transform: translateX(3px);
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.15) !important;
    }

    /* =============================================
       CHAT MESAJLARI — Glassmorphism Balonlar
       ============================================= */
    .stChatMessage {
        border-radius: 14px !important;
        padding: 1rem 1.2rem !important;
        margin-bottom: 0.8rem !important;
        border: 1px solid rgba(255, 255, 255, 0.04) !important;
        animation: messageSlideIn 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    }

    @keyframes messageSlideIn {
        from {
            opacity: 0;
            transform: translateY(12px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Asistan mesajları */
    .stChatMessage[data-testid="assistant-message"],
    .stChatMessage[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        background: rgba(99, 102, 241, 0.06) !important;
        backdrop-filter: blur(12px) !important;
    }

    /* =============================================
       CHAT INPUT — Odaklanma (Focus) Tasarımı
       ============================================= */
    /* Tarayıcı varsayılan kırmızı çerçevesini kaldır ve mor-mavi yap */
    .stChatInput textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
        outline: none !important;
    }

    /* Streamlit'in sarmalayıcı div'indeki kırmızı efekti engelle */
    [data-testid="stChatInput"] > div:focus-within {
        border-color: #6366f1 !important;
        box-shadow: 0 0 10px rgba(99, 102, 241, 0.1) !important;
    }

    .stChatInput button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        border: none !important;
        border-radius: 8px !important;
        color: white !important;
        transition: all 0.3s ease !important;
    }

    .stChatInput button:hover {
        transform: scale(1.1) !important;
        box-shadow: 0 0 12px rgba(99, 102, 241, 0.4) !important;
    }

    /* =============================================
       DURUM KARTI — Menü Aktif Göstergesi
       ============================================= */
    .menu-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(139, 92, 246, 0.15));
        border: 1px solid rgba(99, 102, 241, 0.25);
        color: #a5b4fc;
        padding: 0.35rem 0.8rem;
        border-radius: 8px;
        font-size: 0.8rem;
        font-weight: 500;
        margin: 0.5rem 0;
    }

    .menu-badge-inactive {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        color: rgba(255, 255, 255, 0.3);
        padding: 0.35rem 0.8rem;
        border-radius: 8px;
        font-size: 0.8rem;
        font-weight: 400;
        margin: 0.5rem 0;
    }

    /* =============================================
       SAĞLAYICI DURUM KARTLARI
       ============================================= */
    .provider-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 8px;
        padding: 0.5rem 0.8rem;
        margin-bottom: 0.3rem;
        font-size: 0.78rem;
        color: rgba(255, 255, 255, 0.6);
        transition: all 0.2s ease;
    }

    .provider-card-active {
        background: rgba(99, 102, 241, 0.1);
        border: 1px solid rgba(99, 102, 241, 0.25);
        color: #a5b4fc;
    }

    /* =============================================
       AYIRICI ÇİZGİLER
       ============================================= */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(
            90deg,
            transparent 0%,
            rgba(99, 102, 241, 0.2) 50%,
            transparent 100%
        ) !important;
        margin: 1rem 0 !important;
    }

    /* =============================================
       SCROLLBAR
       ============================================= */
    ::-webkit-scrollbar {
        width: 6px;
    }

    ::-webkit-scrollbar-track {
        background: transparent;
    }

    ::-webkit-scrollbar-thumb {
        background: rgba(99, 102, 241, 0.2);
        border-radius: 3px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: rgba(99, 102, 241, 0.4);
    }

    /* =============================================
       FOOTER
       ============================================= */
    .footer {
        text-align: center;
        padding: 1rem;
        color: rgba(255, 255, 255, 0.3);
        font-size: 0.75rem;
        border-top: 1px solid rgba(255, 255, 255, 0.04);
        margin-top: 2rem;
    }

    .footer a {
        color: rgba(99, 102, 241, 0.6);
        text-decoration: none;
    }

    .footer a:hover {
        color: #6366f1;
    }

    /* =============================================
       İPUCU ALANLARI
       ============================================= */
    .tip-box {
        background: rgba(99, 102, 241, 0.06);
        border-left: 3px solid rgba(99, 102, 241, 0.4);
        border-radius: 0 8px 8px 0;
        padding: 0.6rem 1rem;
        font-size: 0.85rem;
        color: rgba(255, 255, 255, 0.6);
        margin: 0.5rem 0;
    }
</style>
"""
