# 👔 Yusuf Ataş - AI Kariyer Asistanı

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Enabled-1C3C3C?logo=langchain)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Store-orange)
![LLMs](https://img.shields.io/badge/Multi--LLM-OpenAI%20%7C%20Gemini%20%7C%20Groq-success)

Bu proje, Yusuf Ataş'ın profesyonel özgeçmişini, yetkinliklerini, projelerini ve kariyer vizyonunu etkileşimli bir şekilde sunan **RAG (Retrieval-Augmented Generation)** tabanlı yapay zeka destekli bir kariyer asistanıdır. Geleneksel ve statik CV'lerin ötesine geçerek, işe alım uzmanları ve yöneticiler için dinamik, akıllı ve doğal dilde iletişim kurabilen bir profil sistemi sunar.

---

## 📸 Arayüz Önizlemesi

> **[buraya görsel gelecek]**
*(Öneri: Uygulamanın tam ekran bir ekran görüntüsünü veya uygulamanın çalıştığını gösteren kısa bir GIF ekleyin.)*

---

## ✨ Öne Çıkan Özellikler

- 🧠 **Gelişmiş RAG Mimarisi:** Yusuf Ataş'a ait detaylı Markdown bilgi tabanını kullanarak halüsinasyonsuz, %100 doğru ve bağlama uygun yanıtlar üretir.
- ⚡ **Multi-LLM Yönlendirme:** OpenAI, Groq (Llama-3) ve Google Gemini modelleri arasında akıllı geçiş (fallback) yapar. Bir sağlayıcıda sorun çıkarsa diğerine otomatik geçer.
- 🎯 **Niyet Tespiti (Intent Routing):** Kullanıcının sorusunu analiz eder. Menü tabanlı (projeler, deneyimler) özel formatlı soruları tespit edip en optimize zinciri (chain) çalıştırır.
- ✍️ **Yazım Hatası Toleransı (Typo Tolerance):** Kullanıcı sorularındaki ufak harf hatalarını sessizce düzeltir ve akışı bozmadan doğru yanıtı verir.
- 🌊 **Daktilo Efekti (Streaming):** Üretilen yanıtlar ekrana anlık olarak (stream) yansıtılır, kullanıcı deneyimini maksimuma çıkarır.
- 💾 **Akıllı Önbellekleme:** Bilgi tabanı (`.md` dosyası) güncellenmediği sürece vektör veritabanını yeniden oluşturmaz (MD5 Hash tabanlı kontrol).
- ☁️ **Bulut Uyumlu:** Streamlit Cloud üzerinde sorunsuz çalışacak şekilde tasarlanmıştır. HuggingFace Inference API entegrasyonu ile RAM dostudur.

---

## 🏗️ Sistem Mimarisi

> **[<img width="1716" height="800" alt="image" src="https://github.com/user-attachments/assets/a8c88ecc-3ad8-4f24-9fd5-e7462f77989f" />]**

### Kullanılan Teknolojiler
- **Frontend & UI:** Streamlit (Özelleştirilmiş CSS ile)
- **AI / Orkestrasyon:** LangChain & LangGraph mantığı
- **Vektör Veritabanı:** ChromaDB
- **Embedding:** Hugging Face (Local veya Inference API)
- **Dil Modelleri:** OpenAI (GPT-4o), Google GenAI (Gemini 2.0 Flash), Groq (Llama 3)

---

## 💻 Kullanım

> **[<img width="1683" height="937" alt="image" src="https://github.com/user-attachments/assets/92ab3fcf-2f4a-47cc-ba32-97ad774ef582" />]**

Sistem iki şekilde kullanılabilir:
1. **Sol Navigasyon Menüsü:** Hızlı erişim butonları ile Yusuf'un projelerini, deneyimlerini veya eğitim geçmişini listeleyip numara ile detay seçebilirsiniz.
2. **Serbest Sohbet:** Alttaki mesaj kutusuna doğrudan merak ettiğiniz bir soruyu sorabilirsiniz (Örn: *"Zorlu projelerde nasıl bir yol izlersin?"*).

---

## 📬 İletişim

Yusuf Ataş ile teknolojik iş birlikleri ve vizyoner projeler için iletişime geçebilirsiniz:

- **E-posta:** [yusufatas2002@gmail.com](mailto:yusufatas2002@gmail.com)
- **LinkedIn:** [linkedin.com/in/yusuf-atas34](https://www.linkedin.com/in/yusuf-atas34)
- **GitHub:** [github.com/yusufatass](https://github.com/yusufatass)
