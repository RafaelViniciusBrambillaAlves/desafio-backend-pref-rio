from app.application.chatbot.handlers.base_handler import BaseChatbotHandler
from app.application.use_cases.transport_pass.recharge_transport_pass_use_case import RechargeTransportPassUseCase
from app.domain.chatbot_state import ChatbotState
from app.schemas.chatbot_response import ChatbotResponse, ChatbotResponseType
from app.domain.chatbot_intents import ChatbotIntent
from app.repositories.interfaces.chatbot_context_repository_interface import IChatbotContextRepository


class RechargeHandler(BaseChatbotHandler):

    YES = {"sim", "s", "ok", "confirmar"}
    NO = {"não", "nao", "n", "cancelar"}

    def __init__(
            self, 
            recharge_use_case: RechargeTransportPassUseCase, 
            context_repository: IChatbotContextRepository
        ):
        self._recharge_use_case = recharge_use_case
        self._context_repository = context_repository

    async def handle(self, message, user_id, context):
        
        text = message.lower().strip()

        if context.state == ChatbotState.IDLE:
            context.state = ChatbotState.WAITING_RECHARGE_AMOUNT
            await self._context_repository.update(context)

            return ChatbotResponse(
                intent = ChatbotIntent.RECHARGE,
                type = ChatbotResponseType.QUESTION,
                message = "Qual o valor deseja recarregar?"
            )
        
        if context.state == ChatbotState.WAITING_RECHARGE_AMOUNT:

            try:
                amount = float(text.replace(",", "."))
                if amount <= 0:
                    raise ValueError
            except ValueError:
                return ChatbotResponse(
                    intent = ChatbotIntent.RECHARGE,
                    type = ChatbotResponseType.ERROR,
                    message = "Informe um valor válido."
                )
            
            context.temp_amount = amount
            context.state = ChatbotState.CONFIRM_RECHARGE
            await self._context_repository.update(context)

            return ChatbotResponse(
                intent = ChatbotIntent.RECHARGE,
                type = ChatbotResponseType.QUESTION,
                message = f"Confirma recarga de R$ {amount:.2f}? (sim/ não)"
            )
        
        if context.state == ChatbotState.CONFIRM_RECHARGE:

            if text in self.YES and context.temp_amount:

                updated_balance = await self._recharge_use_case.execute(
                    user_id,
                    context.temp_amount  
                )

                await self._context_repository.reset(user_id)

                return ChatbotResponse(
                    intent = ChatbotIntent.RECHARGE,
                    type = ChatbotResponseType.INFO, 
                    message = f"Recarga realizada. Saldo atual: R${updated_balance:.2f}"
                )
            
            if text in self.NO:
                await self._context_repository.reset(user_id)

                return ChatbotResponse(
                    intent = ChatbotIntent.RECHARGE,
                    type = ChatbotResponseType.INFO,
                    message = "Recarga cancelada"
                )
            
            return ChatbotResponse(
                intent = ChatbotIntent.RECHARGE,
                type = ChatbotResponseType.ERROR,
                message = "Responda com 'sim' para confirmar e 'não' para cancelar."
            )