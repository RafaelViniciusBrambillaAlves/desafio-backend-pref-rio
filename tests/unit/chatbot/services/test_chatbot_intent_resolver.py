import pytest
from app.services.chatbot_intent_resolver import ChatbotIntentResolver
from app.domain.chatbot_intents import ChatbotIntent


@pytest.mark.parametrize(
    "message, intent", [
    ("oi", ChatbotIntent.GREETING),
    ("olá", ChatbotIntent.GREETING),
    ("ver saldo", ChatbotIntent.CHECK_BALANCE),
    ("quero recarregar", ChatbotIntent.RECHARGE),
    ("fsdgregew", ChatbotIntent.UNKNOWN),

])
def test_resolve_intent(message, intent):
    
    result = ChatbotIntentResolver.resolve(message)
    
    assert result == intent