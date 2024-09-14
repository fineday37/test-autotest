class MyBaseError(Exception):
    pass


class NotFoundError(MyBaseError):
    pass


class FunctionNotFound(NotFoundError):
    pass


class MyBaseFailure(Exception):
    pass


class ValidationFailure(MyBaseFailure):
    pass


class VariableNotFound(NotFoundError):
    pass


class ParamsError(MyBaseError):
    pass


class CSVNotFound(NotFoundError):
    pass


class EnvNotFound(MyBaseError):
    pass
