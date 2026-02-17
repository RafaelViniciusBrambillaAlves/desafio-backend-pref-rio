from app.domain.chatbot_intents import ChatbotIntent
import re
import unicodedata

class ChatbotIntentResolver:

    KEYWORDS = {
        ChatbotIntent.GREETING: {"oi", "olá", "ola", "bom dia", "boa tarde", "boa noite"},
        ChatbotIntent.CHECK_BALANCE: {"saldo", "ver saldo", "meu saldo"},
        ChatbotIntent.RECHARGE: {"recarga", "recarregar", "colocar credito"}
    }

    @classmethod
    def resolve(cls, message: str) -> ChatbotIntent:
        text = cls._normalize(message)

        for intent, keywords in cls.KEYWORDS.items():
            if any(keyword in text for keyword in keywords):
                return intent

        return ChatbotIntent.UNKNOWN 

        
    @staticmethod
    def _normalize(text: str) -> str:
        text = unicodedata.normalize("NFKD", text)
        text = text.encode("ascii", "ignore").decode("utf-8")
        text = re.sub(r"[^\w\s]", "", text.lower().strip())
        return text