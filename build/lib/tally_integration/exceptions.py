"""
Custom exceptions for Tally Integration Library
"""


class TallyError(Exception):
    """Base exception class for Tally-related errors"""
    pass


class TallyConnectionError(TallyError):
    """Raised when connection to Tally server fails"""
    pass


class TallyAPIError(TallyError):
    """Raised when Tally API returns an error response"""
    def __init__(self, message, status_code=None, response_text=None):
        super().__init__(message)
        self.status_code = status_code
        self.response_text = response_text


class TallyValidationError(TallyError):
    """Raised when input validation fails"""
    pass


class TallyXMLError(TallyError):
    """Raised when XML parsing or construction fails"""
    pass
