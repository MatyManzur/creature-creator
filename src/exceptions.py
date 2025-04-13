class CreatureCreatorError(BaseException):
    def __init__(self, message: str):
        super().__init__(message)

class TimeoutExceededError(CreatureCreatorError):
    def __init__(self):
        super().__init__("Timeout exceeded")

class RetryExceededError(CreatureCreatorError):
    def __init__(self, reason: str = '', retries: int = 0):
        self.reason = reason
        self.retries = retries
        super().__init__("Retry attempts exceeded")

class InvalidResponseError(CreatureCreatorError):
    def __init__(self):
        super().__init__("Unexpected response from server")