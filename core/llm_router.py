"""
Multi-LLM yönlendirici (Router).
OpenAI → Groq → Gemini öncelik sırasıyla fallback mekanizması.
Başarısız sağlayıcılar geçici olarak devre dışı bırakılır.
"""

import time
import logging
from typing import Any

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage

from config import (
    LLM_PROVIDERS,
    LLM_PRIORITY,
    PROVIDER_COOLDOWN_SECONDS,
    LARGE_CONTEXT_TOKEN_THRESHOLD,
    get_available_providers,
)

logger = logging.getLogger(__name__)


def _create_llm(provider_name: str) -> BaseChatModel:
    """Sağlayıcı adına göre LLM instance'ı oluşturur."""
    cfg = LLM_PROVIDERS[provider_name]

    if provider_name == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=cfg["model"],
            temperature=cfg["temperature"],
        )

    elif provider_name == "groq":
        from langchain_groq import ChatGroq
        return ChatGroq(
            model=cfg["model"],
            temperature=cfg["temperature"],
        )

    elif provider_name == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model=cfg["model"],
            temperature=cfg["temperature"],
        )

    raise ValueError(f"Bilinmeyen sağlayıcı: {provider_name}")


class LLMRouter:
    """
    Öncelik tabanlı LLM yönlendirici.
    
    Özellikler:
        - Otomatik fallback: bir sağlayıcı hata verirse sonrakine geçer
        - Cooldown: başarısız sağlayıcılar belirli süre devre dışı kalır
        - Context-aware: büyük context için Gemini tercih edilir
        - Graceful degradation: sadece mevcut API anahtarlarıyla çalışır
    """

    def __init__(self):
        self._available = get_available_providers()
        self._instances: dict[str, BaseChatModel] = {}
        self._failures: dict[str, float] = {}  # provider → son hata zamanı
        self._active_provider: str | None = None

        if not self._available:
            raise EnvironmentError(
                "Hiçbir LLM sağlayıcısı için API anahtarı bulunamadı.\n"
                "En az birini .env dosyanıza ekleyin:\n"
                "  OPENAI_API_KEY=...\n"
                "  GROQ_API_KEY=...\n"
                "  GOOGLE_API_KEY=..."
            )

        logger.info(f"LLM Router başlatıldı. Mevcut sağlayıcılar: {self._available}")

    @property
    def active_provider(self) -> str | None:
        """Şu anda aktif olan sağlayıcının adı."""
        return self._active_provider

    @property
    def available_providers(self) -> list[str]:
        """API anahtarı mevcut olan sağlayıcılar."""
        return list(self._available)

    def _get_instance(self, provider: str) -> BaseChatModel:
        """LLM instance'ını önbellekten al veya oluştur."""
        if provider not in self._instances:
            self._instances[provider] = _create_llm(provider)
        return self._instances[provider]

    def _is_cooled_down(self, provider: str) -> bool:
        """Sağlayıcının cooldown süresinin dolup dolmadığını kontrol eder."""
        if provider not in self._failures:
            return True
        elapsed = time.time() - self._failures[provider]
        return elapsed >= PROVIDER_COOLDOWN_SECONDS

    def _mark_failure(self, provider: str) -> None:
        """Sağlayıcıyı geçici olarak başarısız işaretle."""
        self._failures[provider] = time.time()
        logger.warning(f"⚠️  {provider} başarısız — {PROVIDER_COOLDOWN_SECONDS}s cooldown")

    def _mark_success(self, provider: str) -> None:
        """Sağlayıcıyı başarılı olarak işaretle (cooldown'u temizle)."""
        self._failures.pop(provider, None)
        self._active_provider = provider

    def _get_ordered_providers(self, prefer: str | None = None, context_length: int = 0) -> list[str]:
        """
        Sağlayıcıları öncelik sırasına göre sıralar.
        
        Args:
            prefer: Tercih edilen sağlayıcı (varsa öne alınır)
            context_length: Tahmini context token sayısı
        """
        candidates = [p for p in self._available if self._is_cooled_down(p)]

        if not candidates:
            # Tüm sağlayıcılar cooldown'da — hepsini dene
            candidates = list(self._available)
            logger.warning("Tüm sağlayıcılar cooldown'da — zorla deneniyor")

        # Büyük context → Gemini'yi öne al
        if context_length > LARGE_CONTEXT_TOKEN_THRESHOLD and "gemini" in candidates:
            candidates.remove("gemini")
            candidates.insert(0, "gemini")

        # Tercih edilen sağlayıcıyı öne al
        if prefer and prefer in candidates:
            candidates.remove(prefer)
            candidates.insert(0, prefer)

        return candidates

    def get_llm(self, prefer: str | None = None, context_length: int = 0) -> BaseChatModel:
        """
        Uygun LLM instance'ını döndürür.
        Fallback zincirindeki ilk sağlıklı sağlayıcıyı seçer.
        """
        providers = self._get_ordered_providers(prefer, context_length)
        provider = providers[0]
        self._active_provider = provider
        return self._get_instance(provider)

    def invoke(
        self,
        messages: list[BaseMessage],
        prefer: str | None = None,
        context_length: int = 0,
    ) -> Any:
        """
        Mesajları LLM'e gönderir. Hata durumunda sonraki sağlayıcıyı dener.
        
        Args:
            messages: LLM'e gönderilecek mesajlar
            prefer: Tercih edilen sağlayıcı
            context_length: Tahmini context token sayısı
        
        Returns:
            LLM yanıtı (AIMessage)
        
        Raises:
            RuntimeError: Tüm sağlayıcılar başarısız olursa
        """
        providers = self._get_ordered_providers(prefer, context_length)
        last_error = None

        for provider in providers:
            try:
                llm = self._get_instance(provider)
                logger.info(f"🔄 {provider} ({LLM_PROVIDERS[provider]['model']}) deneniyor...")
                result = llm.invoke(messages)
                self._mark_success(provider)
                logger.info(f"✅ {provider} başarılı")
                return result

            except Exception as e:
                last_error = e
                self._mark_failure(provider)
                logger.error(f"❌ {provider} hatası: {e}")
                continue

        raise RuntimeError(
            f"Tüm LLM sağlayıcıları başarısız oldu.\n"
            f"Denenen: {providers}\n"
            f"Son hata: {last_error}"
        )

    def get_status(self) -> dict[str, str]:
        """Tüm sağlayıcıların durumunu döndürür."""
        status = {}
        for provider in LLM_PRIORITY:
            if provider not in self._available:
                status[provider] = "❌ API anahtarı yok"
            elif not self._is_cooled_down(provider):
                remaining = PROVIDER_COOLDOWN_SECONDS - (time.time() - self._failures[provider])
                status[provider] = f"⏳ Cooldown ({int(remaining)}s)"
            else:
                model = LLM_PROVIDERS[provider]["model"]
                if provider == self._active_provider:
                    status[provider] = f"✅ Aktif ({model})"
                else:
                    status[provider] = f"🟢 Hazır ({model})"
        return status
