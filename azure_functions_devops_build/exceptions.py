class BaseException(Exception):
    def __init__(self, message=None):
        self.message = message


class GitOperationException(BaseException):
    pass