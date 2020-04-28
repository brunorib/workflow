class TokenNotVerifiedException(Exception):
    pass

class TokenAlreadyConsumedException(Exception):
    pass

class TokenWasConsumedByOtherUserException(Exception):
    pass