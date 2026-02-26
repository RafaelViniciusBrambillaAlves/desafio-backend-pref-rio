from fastapi import HTTPException


class AppException(HTTPException):
    def __init__(self, *, error: str, message: str, status_code: int):
        self.error = error
        self.message = message
        
        super().__init__(
            status_code=status_code,
            detail={
                "error": error,
                "message": message
            }
        )
