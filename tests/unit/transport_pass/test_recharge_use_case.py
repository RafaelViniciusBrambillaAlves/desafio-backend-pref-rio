import pytest
from unittest.mock import AsyncMock
from app.application.use_cases.transport_pass.recharge_transport_pass_use_case import RechargeTransportPassUseCase
from app.models.transport_pass import TransportPass
from app.models.transaction import TransactionType
from bson import ObjectId
from app.core.exceptions import AppException
from fastapi import status

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "initial_balance, recharge_amount, expected_balance",
    [
        (10, 7, 17),
        (50, 63, 113), 
        (100, 50, 150),
        (1000, 1, 1001)
    ]
    )
async def test_recharge_sucess(initial_balance, recharge_amount, expected_balance, mock_uow):
    """
    Testando Classe RechargeTransportPassUseCase para recarregar saldo do passe
    """

    # Banco Falso: mock_uow

    user_id = ObjectId()

    # Cria o objeto que tem a regra
    use_case = RechargeTransportPassUseCase(mock_uow)

    # Quando alguém chamar get_by_user_id, finja que o usuário tem saldo 100
    mock_uow.transport_passes.get_by_user_id = AsyncMock(
        return_value = TransportPass(user_id = user_id, balance = initial_balance)
    )

    async def fake_update_balance(user_id, amount):
        return TransportPass(
            user_id = user_id,
            balance = initial_balance + amount
        )

    # Quando atualizar o saldo, retorne um passe com saldo 150
    mock_uow.transport_passes.update_balance = AsyncMock(
        side_effect = fake_update_balance
    )

    mock_uow.transactions.create = AsyncMock()

    # Execute a recarga de 50 reais.
    result = await use_case.execute(user_id, recharge_amount)

    assert result == expected_balance 

    mock_uow.transport_passes.update_balance.assert_called_once_with(
        user_id = user_id,
        amount = recharge_amount
    )

    # Confirma que realmente tentou atualizar no banco e criou a transação
    mock_uow.transport_passes.update_balance.assert_called_once()
    mock_uow.transactions.create.assert_called_once()

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "invalid_amount", 
    [0, -10, -1, -4543]
    )
async def test_recharge_invalid_amount(invalid_amount, mock_uow):
    """
    Testando amount invalido
    """
    
    # Banco Falso: mock_uow

    user_id = ObjectId()

    use_case = RechargeTransportPassUseCase(mock_uow)

    with pytest.raises(AppException) as exc:
        await use_case.execute(user_id, invalid_amount)

    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "recharge_amount, expected_balance",
    [
        (50, 50),
        (10, 10),
        (100, 100),
        (2, 2)
    ]
)
async def test_recharge_creates_transport_pass_if_not_exists(recharge_amount, expected_balance, mock_uow):
    """
    Testado se o usário não tiver passe
    """
    
    # Banco Falso: mock_uow

    user_id = ObjectId()

    use_case = RechargeTransportPassUseCase(mock_uow)

    # Não existe passe
    mock_uow.transport_passes.get_by_user_id = AsyncMock(return_value = None)

    # Quando criar, começa com saldo 0
    mock_uow.transport_passes.create = AsyncMock(
        return_value = TransportPass(user_id = user_id, balance = 0)
    )

    async def fake_update_balance(user_id, amount):
        return TransportPass(
            user_id = user_id,
            balance = amount 
        )

    mock_uow.transport_passes.update_balance = AsyncMock(
        side_effect = fake_update_balance
    )

    mock_uow.transactions.create = AsyncMock()

    result = await use_case.execute(user_id, recharge_amount)

    assert result == expected_balance

    mock_uow.transport_passes.create.assert_called_once()
    mock_uow.transport_passes.update_balance.assert_called_once()
    mock_uow.transactions.create.assert_called_once()
