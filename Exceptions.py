class DbException(Exception):
    pass

class LangException(Exception):
    def __init__(self):
        self.ErrorCode = ""
        self.ErrorMessage = ""
