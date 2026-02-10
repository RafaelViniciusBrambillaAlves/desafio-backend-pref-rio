from app.domain.chatbot_intents import ChatbotIntent
import re

class ChatbotIntentResolver:

    GREETINGS = {"oi", "olá", "ola", "bom dia", "boa tarde", "boa noite"}
    CHECK_BALANCE = {"saldo", "ver saldo", "meu saldo"}
    RECHARGE = {"recarga", "recarregar", "colocar credito"}

    @classmethod
    def resolve(cls, message: str) -> ChatbotIntent:
        text = re.sub(r"[^\w\s]", "", message.lower().strip())

        if cls._match(text, cls.GREETINGS):
            return ChatbotIntent.GREETING
        
        if cls._match(text, cls.CHECK_BALANCE):
            return ChatbotIntent.CHECK_BALANCE
        
        if cls._match(text, cls.RECHARGE):
            return ChatbotIntent.RECHARGE
        
        return ChatbotIntent.UNKNOWN
    
    @staticmethod
    def _match(text: str, keywords: set[str]) -> bool:
        return any(keyword in text for keyword in keywords)