class APIException(Exception):
    """Base API Exception - استثناء API الأساسي"""
    
    def __init__(self, message: str, status_code: int = 400, code: str = 'API_ERROR'):
        self.message = message
        self.status_code = status_code
        self.code = code
        super().__init__(self.message)

class ValidationError(APIException):
    """Validation Error - خطأ التحقق"""
    
    def __init__(self, message: str, details: dict = None):
        self.details = details or {}
        super().__init__(message, 400, 'VALIDATION_ERROR')

class AuthenticationError(APIException):
    """Authentication Error - خطأ المصادقة"""
    
    def __init__(self, message: str = 'Authentication failed'):
        super().__init__(message, 401, 'AUTHENTICATION_ERROR')

class AuthorizationError(APIException):
    """Authorization Error - خطأ التفويض"""
    
    def __init__(self, message: str = 'Access denied'):
        super().__init__(message, 403, 'AUTHORIZATION_ERROR')

class NotFoundError(APIException):
    """Not Found Error - خطأ عدم وجود"""
    
    def __init__(self, resource: str):
        super().__init__(f'{resource} not found', 404, 'NOT_FOUND')

class ConflictError(APIException):
    """Conflict Error - خطأ تضارب"""
    
    def __init__(self, message: str):
        super().__init__(message, 409, 'CONFLICT')
