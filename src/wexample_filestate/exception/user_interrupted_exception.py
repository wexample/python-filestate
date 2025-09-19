from wexample_helpers.exception.undefined_exception import UndefinedException


class UserInterruptedException(UndefinedException):
    error_code: str = "USER_INTERRUPTED_EXCEPTION"
