# exceptions.py
class APIError(Exception):
    """Base exception for API errors"""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class ConfigurationError(APIError):
    """Raised when there's a configuration issue"""
    pass

class ValidationError(APIError):
    """Raised when request validation fails"""
    pass

