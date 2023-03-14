class SortMapNotFoundException(Exception):
    def __init__(self):
        self.message = "There is no SortMap with that ID"


class SortMapValueNotValidException(Exception):
    def __init__(self):
        self.message = "A SortMap must be a string of digits only (0123456789) and can not have duplicates in it"


class MessageToEncryptNotValidException(SortMapValueNotValidException):
    pass
