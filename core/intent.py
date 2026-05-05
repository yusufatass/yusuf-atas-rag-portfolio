"""
Intent (niyet) tespit motoru ve menü yönetimi.
chat.py'deki tüm intent/menü mantığı burada merkezileştirilmiştir.
"""


# ==========================================
# SABİT VERİ KAYNAKLARI (.md ile senkron)
# ==========================================

PROJE_LISTESI = {
    "1":  "Akbank GenAI Bootcamp Projesi",
    "2":  "Cligomate - Ideathon Projesi",
    "3":  "AI Startup Scout Projesi",
    "4":  "Müşteri Kaybı (Churn) Analizi Projesi",
    "5":  "IMDb Yorumları Duygu Analizi Projesi",
    "6":  "YouTube AI Scraping Agent Projesi",
    "7":  "AI Newsletter Agent",
    "8":  "Document Chatbot (RAG)",
    "9":  "To-Do with Gemini Projesi",
    "10": "Akıllı Hava Durumu Projesi",
    "11": "Blue Pery: Dijital Marka Dönüşümü ve E-Ticaret Altyapısı",
    "12": "BURD: Android Tabanlı Seyahat ve Tur Yönetim Platformu",
}

DENEYIM_LISTESI = {
    "1": "Logo Yazılım - Veri Bilimi Departmanı (Stajyer)",
    "2": "Sınav Dershanesi - Matematik Öğretmenliği",
}

SERTIFIKA_LISTESI = {
    "1": "Yapay Zeka ve Teknoloji Akademisi (AI Fellowship)",
    "2": "McKinsey Forward (Professional Development Program)",
    "3": "Akbank Generative AI Bootcamp",
    "4": "Google Project Management Professional Certificate",
    "5": "Google Data Analytics: Foundations",
    "6": "Coderspace - Siber Güvenlik Okulu",
}

MULAKAT_LISTESI = {
    "1": "Beklenmedik bir kriz veya stresli bir durumla nasıl başa çıkar?",
    "2": "Hiç başarısız olduğu bir an oldu mu? Bu durumdan ne öğrendi?",
    "3": "Ekip içinde bir fikir çatışması yaşandığında tavrı ne olur?",
    "4": "Kendini eleştirdiği veya geliştirmesi gerektiğini düşündüğü yönleri nelerdir?",
    "5": "Neden 2002 doğumlu genç bir mühendisi kıdemli birinin yerine tercih etmeliyiz?",
    "6": "Bir yöneticiyle fikir ayrılığına düştüğünde tavrı ne olur?",
    "7": "Motivasyonu düştüğünde onu ne ayağa kaldırır?",
    "8": "Belirsizliğin yüksek olduğu projelerde nasıl ilerler?",
    "9": "Kendinde en güçlü bulduğu özellik nedir?",
}

# Menü türü → (sözlük, metadata_key)
MENU_CONFIG = {
    "proje":     (PROJE_LISTESI,     "Proje_Detay"),
    "deneyim":   (DENEYIM_LISTESI,   "Alt_Bolum"),
    "sertifika": (SERTIFIKA_LISTESI, "Alt_Bolum"),
    "mulakat":   (MULAKAT_LISTESI,   "Alt_Bolum"),
}

# Blok bölüm sorguları — tüm chunk'ları metadata filtresiyle çekeriz
BOLUM_SORGULARI = {
    "hobiler":      "8. İLGİ ALANLARI VE YAŞAM STİLİ",
    "ilgi":         "8. İLGİ ALANLARI VE YAŞAM STİLİ",
    "yaşam":        "8. İLGİ ALANLARI VE YAŞAM STİLİ",
    "karakter":     "7. KİŞİLİK VE KARAKTERİSTİK YAPI",
    "vizyon":       "7. KİŞİLİK VE KARAKTERİSTİK YAPI",
    "kişilik":      "7. KİŞİLİK VE KARAKTERİSTİK YAPI",
    "akademik":     "5. AKADEMİK EĞİTİM",
    "eğitim":       "5. AKADEMİK EĞİTİM",
    "üniversite":   "5. AKADEMİK EĞİTİM",
    "kimlik":       "1. KİMLİK VE GENEL ÖZET",
    "genel":        "1. KİMLİK VE GENEL ÖZET",
    "teknik":       "2. TEKNİK YETKİNLİKLER",
    "yetkinlik":    "2. TEKNİK YETKİNLİKLER",
    # İletişim & Sosyal Medya
    "iletişim":     "10. İLETİŞİM BİLGİLERİ",
    "iletişime":    "10. İLETİŞİM BİLGİLERİ",
    "ulaş":         "10. İLETİŞİM BİLGİLERİ",
    "ulaşmak":      "10. İLETİŞİM BİLGİLERİ",
    "e-posta":      "10. İLETİŞİM BİLGİLERİ",
    "eposta":       "10. İLETİŞİM BİLGİLERİ",
    "email":        "10. İLETİŞİM BİLGİLERİ",
    "mail":         "10. İLETİŞİM BİLGİLERİ",
    "linkedin":     "10. İLETİŞİM BİLGİLERİ",
    "github":       "10. İLETİŞİM BİLGİLERİ",
    "kaggle":       "10. İLETİŞİM BİLGİLERİ",
    "sosyal":       "10. İLETİŞİM BİLGİLERİ",
    "profil":       "10. İLETİŞİM BİLGİLERİ",
    "contact":      "10. İLETİŞİM BİLGİLERİ",
    "lokasyon":     "10. İLETİŞİM BİLGİLERİ",
    "adres":        "10. İLETİŞİM BİLGİLERİ",
    "telefon":      "10. İLETİŞİM BİLGİLERİ",
    # Dil becerileri
    "dil":          "11. DİLLER (LANGUAGE PROFICIENCY)",
    "diller":       "11. DİLLER (LANGUAGE PROFICIENCY)",
    "language":     "11. DİLLER (LANGUAGE PROFICIENCY)",
    "ingilizce":    "11. DİLLER (LANGUAGE PROFICIENCY)",
    "almanca":      "11. DİLLER (LANGUAGE PROFICIENCY)",
}

# ==========================================
# ANAHTAR KELİME SETLERİ (Intent Detection)
# ==========================================

PROJE_ANAHTAR = {
    "proje", "projeler", "portföy", "portfolio",
    "yaptığın", "geliştirdiğin", "çalışmaların",
    "neler yaptı", "neler geliştirdi", "hangi projeler",
    "çalışmalar", "uygulamalar", "sistemler",
}

DENEYIM_ANAHTAR = {
    "deneyim", "deneyimler", "iş deneyimi", "çalıştı", "çalışma",
    "staj", "stajı", "stajyer", "iş hayatı", "kariyer",
    "profesyonel geçmiş", "nerede çalıştı", "iş geçmişi",
    "çalıştığı", "çalıştığın",
}

SERTIFIKA_ANAHTAR = {
    "sertifika", "sertifikalar", "kurs", "program",
    "bootcamp", "mckinsey", "coursera",
    "gelişim", "aldığı", "tamamladığı", "bitirdiği",
}

MULAKAT_ANAHTAR = {
    "mülakat", "mülakatlar", "mülakat sorusu", "mülakat soruları",
    "soru", "sorular", "ik soruları", "davranışsal",
    "star tekniği", "interview", "kriz", "hr", "human resource",
}

BOLUM_ANAHTAR = set(BOLUM_SORGULARI.keys())

# ==========================================
# YARDIMCI SÖZLÜK HARİTALARI
# ==========================================

SOZLUK_MAP = {k: v[0] for k, v in MENU_CONFIG.items()}
METADATA_KEY_MAP = {k: v[1] for k, v in MENU_CONFIG.items()}


def _liste_metni(sozluk: dict) -> str:
    """Sözlükten numaralı liste metni oluşturur."""
    return "\n".join(f"  {k}. {v}" for k, v in sozluk.items())


MENU_METNI_MAP = {k: _liste_metni(v[0]) for k, v in MENU_CONFIG.items()}

MENU_MESAJ_MAP = {
    "proje": (
        "Yusuf Bey, yapay zeka ve veri bilimi odaklı birçok inovatif proje geliştirmiştir. "
        "İşte aşağıda detaylarını inceleyebileceğiniz projelerin listesi:\n\n"
        f"{_liste_metni(PROJE_LISTESI)}\n\n"
        "Hangi proje hakkında daha fazla detay öğrenmek istersiniz? "
        "Numarasını veya proje adını yazabilirsiniz."
    ),
    "deneyim": (
        "Yusuf Bey'in profesyonel geçmişi ve iş deneyimleri hakkında detaylı bilgiye aşağıdan ulaşabilirsiniz:\n\n"
        f"{_liste_metni(DENEYIM_LISTESI)}\n\n"
        "İlginizi çeken deneyimin numarasını veya ismini belirtebilirsiniz."
    ),
    "sertifika": (
        "Yusuf Bey, küresel programlar ve prestijli kurumlardan birçok sertifika ve eğitim başarısına sahiptir. "
        "Detaylarını merak ettiğiniz başlığı aşağıdan seçebilirsiniz:\n\n"
        f"{_liste_metni(SERTIFIKA_LISTESI)}\n\n"
        "Hangi sertifika hakkında detaylı bilgi almak istersiniz?"
    ),
    "mulakat": (
        "Yusuf Bey'in vizyonunu, kriz yönetimini ve profesyonel duruşunu anlamak için aşağıdaki mülakat başlıklarını inceleyebilirsiniz:\n\n"
        f"{_liste_metni(MULAKAT_LISTESI)}\n\n"
        "Merak ettiğiniz sorunun numarasını yazarak yanıtını görebilirsiniz."
    ),
}


# ==========================================
# INTENT TESPİT FONKSİYONLARI
# ==========================================

def _spesifik_isim_var_mi(soru_lower: str, sozluk: dict) -> bool:
    """Soruda, listedeki bir öğenin spesifik adı geçiyor mu?"""
    for isim in sozluk.values():
        if len(isim) < 15:
            continue
        uzun = [k for k in isim.lower().split() if len(k) > 5]
        if any(k in soru_lower for k in uzun):
            return True
    return False


def intent_tespit(soru: str) -> str:
    """
    Kullanıcı sorusunun niyetini tespit eder.
    
    Dönüş değerleri:
        "proje_menu"  | "deneyim_menu" | "sertifika_menu" |
        "mulakat_menu" | "bolum_blok:<bolum_adi>" | "rag"
    """
    s = soru.lower()

    # Spesifik isim varsa direkt RAG
    for sozluk in [PROJE_LISTESI, DENEYIM_LISTESI, SERTIFIKA_LISTESI, MULAKAT_LISTESI]:
        if _spesifik_isim_var_mi(s, sozluk):
            return "rag"

    # Bölüm blok sorgusu (hobiler, karakter, akademik vb.)
    for anahtar, bolum_adi in BOLUM_SORGULARI.items():
        if anahtar in s:
            return f"bolum_blok:{bolum_adi}"

    # Menü yönlendirmeleri
    if any(a in s for a in MULAKAT_ANAHTAR):
        return "mulakat_menu"
    if any(a in s for a in DENEYIM_ANAHTAR):
        return "deneyim_menu"
    if any(a in s for a in SERTIFIKA_ANAHTAR):
        return "sertifika_menu"
    if any(a in s for a in PROJE_ANAHTAR):
        return "proje_menu"

    return "rag"


def secim_coz(soru: str, sozluk: dict) -> str | None:
    """
    Numara veya kısmi isimden tam ismi çözer.
    Bulamazsa None döner → menüde kal.
    """
    s = soru.strip()

    # Direkt numara eşleşmesi
    if s in sozluk:
        return sozluk[s]

    s_lower = s.lower()

    # Tam / kısmi string eşleşmesi
    for isim in sozluk.values():
        if s_lower in isim.lower() or isim.lower() in s_lower:
            return isim

    # Uzun kelime eşleşmesi (>3 karakter)
    for isim in sozluk.values():
        uzun = [k for k in isim.lower().split() if len(k) > 3]
        if any(k in s_lower for k in uzun):
            return isim

    return None
