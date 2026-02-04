from urllib.parse import urlencode
from os import getenv
from app.core.config import settings

class GoogleOAuth:
    AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    TOKEN_URL = "https://oauth2.googleapis.com/token"
    USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

    def __init__(self):
        self.client_id = settings.GOOGLE_CLIENT_ID
        self.redirect_uri = settings.GOOGLE_REDIRECT_URI

    def get_authorization_url(self) -> str:
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": "openid email profile", 
            "access_type": "offline",
            "prompt": "consent"
        }
        return f"{self.AUTH_URL}?{urlencode(params)}"

google_oauth = GoogleOAuth()