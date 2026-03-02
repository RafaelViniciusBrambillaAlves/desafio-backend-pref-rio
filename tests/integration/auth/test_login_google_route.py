import pytest
from unittest.mock import AsyncMock, patch
from fastapi import status

@pytest.mark.asyncio
async def test_google_login_redirect(client):

    with patch(
        "app.core.oauth.google.google_oauth.get_authorization_url",
        return_value = "https://accounts.google.com/test"
    ):
        response = await client.get(
            "/auth/google/login",
            follow_redirects = False
        )

    assert response.status_code in (status.HTTP_302_FOUND, status.HTTP_307_TEMPORARY_REDIRECT)
    assert response.headers["location"] == "https://accounts.google.com/test"