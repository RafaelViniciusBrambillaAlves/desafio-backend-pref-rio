import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.dependencies.database_dependencies import get_unit_of_work
from unittest.mock import AsyncMock
from app.models.user import User
from bson import ObjectId
from app.dependencies.database_dependencies import get_unit_of_work
from app.core.auth_dependencies import get_current_user
from app.dependencies.transport_pass_dependecies import get_recharge_use_case
from fastapi import status
from app.core.exceptions import AppException

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "amount, expected_status, expected_balance",
    [
        (50, status.HTTP_200_OK, 150),
        (10, status.HTTP_200_OK, 110),
        (0, status.HTTP_400_BAD_REQUEST, None),
        (-5, status.HTTP_400_BAD_REQUEST, None)
    ]
)
async def test_recharge_route_success(amount, expected_status, expected_balance):
    """
    Testando Rota 
    - '/transport-pass/recharge'
    """

    # Mock User
    fake_user = User(
        id = ObjectId(),
        email = "test@test.com"
        )

    async def override_get_current_user():
        return fake_user
   
    # Mock Uow
    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow
    mock_uow.__aexit__.return_value = None

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
     
    # Overrides 
    app.dependency_overrides[get_current_user] = override_get_current_user
    app.dependency_overrides[get_unit_of_work] = override_get_uow
    app.dependency_overrides[get_recharge_use_case] = override_get_use_case

    transport = ASGITransport(app = app)

    async with AsyncClient(
        transport = transport,
        base_url = "http://test"
    ) as client:
        
        response = await client.post(
            "/transport-pass/recharge",
            json = {"amount": amount}
        )


    # Asserts 
    assert response.status_code == expected_status

    if expected_status == status.HTTP_200_OK:
        assert response.json()["data"]["balance"] == expected_balance
        mock_use_case.execute.assert_called_once_with(
            fake_user.id,
            amount
        )
    
    app.dependency_overrides.clear()
    
