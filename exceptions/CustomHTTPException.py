from fastapi import HTTPException


class CustomHTTPException(HTTPException):
    def __init__(self, status_code: int, error_message: int):
        super().__init__(status_code=status_code, detail={"error": error_message})
        self.error_message = error_message
