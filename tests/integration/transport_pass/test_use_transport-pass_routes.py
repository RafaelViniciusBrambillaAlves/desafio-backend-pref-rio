import pytest
from fastapi import status
from app.models.user import User
from bson import ObjectId
from unittest.mock import AsyncMock
from app.core.exceptions import AppException
from app.main import app
from app.core.auth_dependencies import get_current_user
from app.dependencies.database_dependencies import get_unit_of_work
from app.dependencies.transport_pass_dependecies import get_use_transport_use_case
from httpx import AsyncClient, ASGITransport


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "amount, expected_status, expected_balance",
    [
        (5, status.HTTP_200_OK, 95),
        (1, status.HTTP_200_OK, 99),
        (0, status.HTTP_422_UNPROCESSABLE_CONTENT, None),
        (-10, status.HTTP_422_UNPROCESSABLE_CONTENT, None)
    ]
)
async def test_use_transport_route(client, mock_uow, amount, expected_status, expected_balance):
    """
    Testando rota:
    POST /transport-pass/use
    """

    # Fake user
    fake_user = User(
        id = ObjectId(),
        email = "test@test.com"
    )

    async def override_get_current_user():
        return fake_user

    async def override_get_uow():
        return mock_uow
    
    # Mock Use Case
    mock_use_case = AsyncMock()

    if amount > 0:
        mock_use_case.execute.return_value = expected_balance
    else:
        mock_use_case.execute.side_effect = AppException(
            status_code = status.HTTP_400_BAD_REQUEST,
            message = "Invalid amount",
            error = "INVALID_AMOUNT"
        )
    
    async def override_get_use_case():
        return mock_use_case
    
    # Dependency overrides 
    app.dependency_overrides[get_current_user] = override_get_current_user
    app.dependency_overrides[get_unit_of_work] = override_get_uow
    app.dependency_overrides[get_use_transport_use_case] = override_get_use_case

    try:
        response = await client.post(
            "/transport-pass/use",
            json = {"amount": amount}
        )

        # Assertions
        assert response.status_code == expected_status

        if expected_status == status.HTTP_200_OK:
            assert response.json()["data"]["balance"] == expected_balance

            mock_use_case.execute.assert_called_once_with(
                fake_user.id,
                amount
            )

    finally:
        
        app.dependency_overrides.clear()
