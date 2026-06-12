class BotBaseException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class NetworkException(BotBaseException):
    """ Network error """
    pass

class BadResponseException(BotBaseException):
    """ Uncorrect data """
    pass

class LLMException(BotBaseException):
    """ API error """
    pass


