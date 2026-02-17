# from app.domain.chatbot_intents import ChatbotIntent
# from app.services.chatbot_intent_resolver import ChatbotIntentResolver
# from bson import ObjectId
# # from app.repositories.transport_pass_repository import TransportPassRepository
# from app.schemas.chatbot_response import ChatbotResponse, ChatbotResponseType
# # from app.repositories.chatbot_context_repository import ChatbotContextRepository
# from app.domain.chatbot_state import ChatbotState
# from app.services.transport_pass_services import TransportPassService
# from app.repositories.interfaces.chatbot_context_repository_interface import IChatbotContextRepository


# class ChatbotService:

#     YES = {"sim", "s", "ok", "confirmar", "confirmo"}
#     NO = {"não", "nao", "n", "cancelar"}

#     def __init__(
#             self,
#             context_repository: IChatbotContextRepository,
#             transport_service: TransportPassService 
#     ):
#         self.context_repository = context_repository
#         self.transport_service = transport_service

#     async def handle_message(self, message: str, user_id: ObjectId):
#         context = await self.context_repository.get(user_id)
#         text = message.lower().strip()

#         if context.state == ChatbotState.CONFIRM_RECHARGE:
#             return await self._handle_recharge_confirmation(text, context)

#         if context.state == ChatbotState.WAITING_RECHARGE_AMOUNT:
#             return await self._handle_recharge_amount(text, context)

#         intent = ChatbotIntentResolver.resolve(message)

#         match intent:
#             case ChatbotIntent.GREETING:
#                 return ChatbotResponse(
#                     intent = intent,
#                     type = ChatbotResponseType.INFO,
#                     message = "Olá! Posso te ajudar com o saldo ou recarga."
#                 )

#             case ChatbotIntent.RECHARGE:
#                 context.state = ChatbotState.WAITING_RECHARGE_AMOUNT
#                 await self.context_repository.update(context)

#                 return ChatbotResponse(
#                     intent = intent,
#                     type = ChatbotResponseType.QUESTION,
#                     message = "Qual o valor você deseja recarregar?"
#                 )
            
#             case ChatbotIntent.CHECK_BALANCE:
#                 balance = await self.transport_service.get_balance(user_id)

#                 return ChatbotResponse(
#                     intent = intent,
#                     type = ChatbotResponseType.INFO,
#                     message = f"O seu saldo atual é de {balance:.2f}"
#                 )
            
#             case _:
#                 return ChatbotResponse(
#                     intent = "unknown",
#                     type = ChatbotResponseType.ERROR,
#                     message = "Não entendi. Você pode perguntar sobre saldo ou recarga."
#                 )

#     async def _handle_recharge_amount(self, message: str, context):
#         try:
#             amount = float(message.replace(",", "."))
#         except ValueError:
#             return ChatbotResponse(
#                 intent = "recharge",
#                 type = ChatbotResponseType.ERROR,
#                 message = "Informe um valor válido para recarga."
#             )
        
#         if amount <= 0:
#             return ChatbotResponse(
#                 intent = "recharge",
#                 type = ChatbotResponseType.ERROR,
#                 message = "Informe um valor válido para recarga."
#             )

#         context.temp_amount = amount
#         context.state = ChatbotState.CONFIRM_RECHARGE
#         await self.context_repository.update(context)

#         return  ChatbotResponse(
#             intent = "recharge",
#             type = ChatbotResponseType.QUESTION,
#             message = f"Confirme a recarga de R$ {amount:.2f}? (sim/ não)"
#         )
    
#     async def _handle_recharge_confirmation(self, text: str, context):
#         if text in self.YES:
#             amount = context.temp_amount

#             update_balance = await self.transport_service.recharge(
#                 context.user_id,
#                 amount
#             )

#             await self.context_repository.reset(context.user_id)

#             return ChatbotResponse(
#                 intent = "recharge", 
#                 type = ChatbotResponseType.INFO,
#                 message = (
#                     f"Recarga de R$ {amount:.2f} realizada com sucesso.\n"
#                     f"Saldo atual: R$ {update_balance:.2f}"
#                 )
#             )

#         if text in self.NO:
#             await self.context_repository.reset(context.user_id)

#             return ChatbotResponse(
#                 intent = "recharge", 
#                 type = ChatbotResponseType.INFO,
#                 message = "Recarga cancela. Posso te ajudar em algo mais?"
#             )
        
#         return ChatbotResponse(
#             intent = "recharge",
#             type = ChatbotResponseType.ERROR,
#             message = "Responda com 'sim' para confirmar ou 'não' para cancelar." 
#         )