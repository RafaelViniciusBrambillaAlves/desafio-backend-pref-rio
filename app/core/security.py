from passlib.context import CryptContext

class Security():
    pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

    @staticmethod
    def hash_password(password: str) -> str:
        return Security.pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> str:
        return Security.pwd_context.verify(plain_password, hashed_password)