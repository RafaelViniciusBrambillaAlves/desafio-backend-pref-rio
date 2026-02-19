from app.application.chatbot.handlers.base_handler import BaseChatbotHandler
from app.application.use_cases.transport_pass.recharge_transport_pass_use_case import RechargeTransportPassUseCase
from app.domain.chatbot_state import ChatbotState
from app.schemas.chatbot_response import ChatbotResponse, ChatbotResponseType
from app.domain.chatbot_intents import ChatbotIntent
from app.repositories.interfaces.chatbot_context_repository_interface import IChatbotContextRepository


class RechargeHandler(BaseChatbotHandler):

    YES = {"sim", "s", "ok", "confirmar"}
    NO = {"não", "nao", "n"}
    CANCEL = {"cancelar", "voltar", "sair"}

    def __init__(self, recharge_use_case: RechargeTransportPassUseCase):
        self._recharge_use_case = recharge_use_case

    async def handle(self, message, user_id, context, uow):
        
        text = message.lower().strip()

        if context.state == ChatbotState.IDLE:

            return ChatbotResponse(
                intent = ChatbotIntent.RECHARGE,
                type = ChatbotResponseType.QUESTION,
                message = "Qual o valor deseja recarregar?",
                next_state = ChatbotState.WAITING_RECHARGE_AMOUNT
            )
        
        if context.state == ChatbotState.WAITING_RECHARGE_AMOUNT:
            if text in self.CANCEL:
                return ChatbotResponse(
                    intent = ChatbotIntent.RECHARGE,
                    type = ChatbotResponseType.INFO,
                    message = "Recarga cancelada.",
                    reset_context = True
                )

            try:
                amount = float(text.replace(",", "."))
                if amount <= 0:
                    raise ValueError
            except ValueError:
                return ChatbotResponse(
                    intent = ChatbotIntent.RECHARGE,
                    type = ChatbotResponseType.ERROR,
                    message = "Informe um valor válido ou cancele."
                )

            return ChatbotResponse(
                intent = ChatbotIntent.RECHARGE,
                type = ChatbotResponseType.QUESTION,
                message = f"Confirma recarga de R$ {amount:.2f}? (sim/ não)",
                next_state = ChatbotState.CONFIRM_RECHARGE,
                temp_amount = amount
            )
        
        if context.state == ChatbotState.CONFIRM_RECHARGE:

            if text in self.YES and context.temp_amount is not None:

                updated_balance = await self._recharge_use_case.execute(
                    uow,
                    user_id,
                    context.temp_amount  
                )

                return ChatbotResponse(
                    intent = ChatbotIntent.RECHARGE,
                    type = ChatbotResponseType.INFO, 
                    message = f"Recarga realizada. Saldo atual: R${updated_balance:.2f}",
                    reset_context = True
                )
            
            if text in self.NO:

                return ChatbotResponse(
                    intent = ChatbotIntent.RECHARGE,
                    type = ChatbotResponseType.INFO,
                    message = "Recarga cancelada",
                    reset_context = True
                )
            
            return ChatbotResponse(
                intent = ChatbotIntent.RECHARGE,
                type = ChatbotResponseType.ERROR,
                message = "Responda com 'sim' para confirmar e 'não' para cancelar."
            )